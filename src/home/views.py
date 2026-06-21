from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django_filters.views import FilterView
from Processos.filters import ProcessoFilter
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Avg, Min, Max, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractDay
from django.utils import timezone
import datetime
import json
from Usuarios.models import Notificacao, UserProfile

from .forms import SignUpForm
from Processos.models import ProcessoLegislativo, TermoMonitorado
from Processos.services import sync_processo_on_demand


class ProcessoDetailView(LoginRequiredMixin, DetailView):
    model = ProcessoLegislativo
    template_name = "home/proposicao_detalhes.html"
    context_object_name = "processo"

    def get_queryset(self):
        return ProcessoLegislativo.objects.prefetch_related('movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "proposicoes"
        
        is_favorito = TermoMonitorado.objects.filter(
            users=self.request.user,
            processos=self.object
        ).exists()
        context["is_favorito"] = is_favorito
        
        sync_processo_on_demand(self.object)
        return context

class DashboardView(TemplateView):
    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "dashboard"
        
        # Tempo médio de tramitação
        qs = ProcessoLegislativo.objects.annotate(
            primeira_movimentacao=Min('movimentacoes__data_evento')
        ).filter(primeira_movimentacao__isnull=False).annotate(
            dias_tramitacao=ExpressionWrapper(
                ExtractDay(timezone.now() - F('primeira_movimentacao')),
                output_field=fields.IntegerField()
            )
        )
        tempo_medio = qs.aggregate(media=Avg('dias_tramitacao'))['media']
        context["tempo_medio"] = tempo_medio if tempo_medio is not None else 0

        # Estagnados vs Em andamento
        estagnados = Notificacao.objects.filter(tipo='ESTAGNACAO').values('processo').distinct().count()
        total_processos = ProcessoLegislativo.objects.count()
        context["estagnados"] = estagnados
        context["em_andamento"] = total_processos - estagnados

        return context


class ProcessosView(LoginRequiredMixin, FilterView):
    template_name = "home/processos.html"
    model = ProcessoLegislativo
    context_object_name = "processos"
    paginate_by = 10
    filterset_class = ProcessoFilter

    def get_queryset(self):
        qs = ProcessoLegislativo.objects.all().order_by('-ano', '-numero')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "processos"
        
        # Para saber quais processos o usuário já favoritou na view
        favoritos_ids = ProcessoLegislativo.objects.filter(
            termos_monitorados__users=self.request.user
        ).values_list('id', flat=True)
        context["favoritos_ids"] = list(favoritos_ids)
        
        # NOTA: A sincronização on-demand foi movida para o endpoint
        # /processos/<pk>/sync-status/ e é feita de forma assíncrona
        # via HTMX para não bloquear o carregamento da página.
        
        return context


class ProcessoSyncStatusView(LoginRequiredMixin, View):
    """Endpoint HTMX: sincroniza um processo com a API e retorna o partial
    HTML da linha completa (<tr>) para substituição via hx-swap='outerHTML'."""

    def get(self, request, pk, *args, **kwargs):
        processo = get_object_or_404(ProcessoLegislativo, pk=pk)
        sync_processo_on_demand(processo)
        # Recarrega do banco para garantir dados frescos após sync
        processo.refresh_from_db()

        is_favorito = TermoMonitorado.objects.filter(
            users=request.user,
            processos=processo
        ).exists()

        return render(request, 'home/partials/processo_row_status.html', {
            'processo': processo,
            'is_favorito': is_favorito,
        })


class FavoritosView(LoginRequiredMixin, ListView):
    template_name = "home/favoritos.html"
    context_object_name = "favoritos"

    def get_queryset(self):
        base_qs = ProcessoLegislativo.objects.filter(
            termos_monitorados__users=self.request.user
        ).distinct()
        
        # Sincroniza os favoritos antes de calcular os metadados e filtros
        for processo in base_qs:
            sync_processo_on_demand(processo)
            
        qs = base_qs.prefetch_related('movimentacoes')
        
        status = self.request.GET.get('status', 'todas')
        limite = timezone.now() - datetime.timedelta(days=30)
        
        qs = qs.annotate(ultima_mov=Max('movimentacoes__data_evento'))
        
        if status == 'estagnadas':
            qs = qs.filter(ultima_mov__lt=limite)
        elif status == 'tramitacao_normal':
            qs = qs.filter(ultima_mov__gte=limite)
        elif status == 'urgencia':
            qs = qs.filter(notificacoes__lida=False).distinct()
            
        return qs.order_by('-ultima_mov')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "favoritos"
        context["status_atual"] = self.request.GET.get('status', 'todas')
        
        base_qs = ProcessoLegislativo.objects.filter(
            termos_monitorados__users=self.request.user
        ).distinct()
        
        qs_annotated = base_qs.annotate(ultima_mov=Max('movimentacoes__data_evento'))
        
        limite = timezone.now() - datetime.timedelta(days=30)
        
        # Original Favoritos KPI
        context["total_count"] = qs_annotated.count()
        context["normal_count"] = qs_annotated.filter(ultima_mov__gte=limite).count()
        context["estagnadas_count"] = qs_annotated.filter(ultima_mov__lt=limite).count()
        context["urgencia_count"] = qs_annotated.filter(notificacoes__lida=False).distinct().count()
        
        # Processos/Proposicoes KPI that were moved here
        context["total_pls"] = base_qs.count()
        context["em_tramitacao"] = base_qs.exclude(status_atual__icontains='aprovad').exclude(status_atual__icontains='arquivad').count()
        context["aprovadas"] = base_qs.filter(status_atual__icontains='aprovad').count()
        context["com_alerta"] = Notificacao.objects.filter(user=self.request.user, lida=False).values('processo').distinct().count()
        
        return context


class AlertasView(LoginRequiredMixin, ListView):
    template_name = "home/alertas.html"
    model = Notificacao
    context_object_name = "notificacoes"

    def get_queryset(self):
        return Notificacao.objects.filter(user=self.request.user).order_by('-data_criacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "alertas"
        
        qs = ProcessoLegislativo.objects.annotate(
            primeira_movimentacao=Min('movimentacoes__data_evento')
        ).filter(primeira_movimentacao__isnull=False).annotate(
            dias_tramitacao=ExpressionWrapper(
                ExtractDay(timezone.now() - F('primeira_movimentacao')),
                output_field=fields.IntegerField()
            )
        )
        tempo_medio = qs.aggregate(media=Avg('dias_tramitacao'))['media']
        context["tempo_medio_comissoes"] = int(tempo_medio) if tempo_medio is not None else 0
        
        context["volume_estagnacao"] = Notificacao.objects.filter(
            user=self.request.user, tipo='ESTAGNACAO'
        ).count()
        
        context["urgencia_temporal"] = Notificacao.objects.filter(
            user=self.request.user, lida=False
        ).count()
        
        return context


class UsuarioView(LoginRequiredMixin, TemplateView):
    template_name = "home/usuario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "usuario"
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        context["profile"] = profile
        return context

    def post(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        
        receber_estagnacao = request.POST.get('receber_alertas_estagnacao') == 'on'
        dias_estagnacao = request.POST.get('dias_limite_estagnacao', 30)
        receber_novas_mov = request.POST.get('receber_alertas_novas_movimentacoes') == 'on'
        
        profile.receber_alertas_estagnacao = receber_estagnacao
        try:
            profile.dias_limite_estagnacao = int(dias_estagnacao)
        except ValueError:
            profile.dias_limite_estagnacao = 30
        profile.receber_alertas_novas_movimentacoes = receber_novas_mov
        
        profile.save()
        
        context = self.get_context_data()
        context["success"] = True
        return self.render_to_response(context)

class BuscarProposicaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        if not q:
            return JsonResponse({'results': []})
        
        qs = ProcessoLegislativo.objects.filter(
            models.Q(ementa__icontains=q) | 
            models.Q(numero__icontains=q) |
            models.Q(id_externo__icontains=q)
        )[:20]
        
        results = [
            {
                'id': p.id,
                'titulo': f"{p.tipo_proposicao} {p.numero}/{p.ano}",
                'ementa': p.ementa
            } for p in qs
        ]
        return JsonResponse({'results': results})

class AcompanharProposicaoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        proposicao_id = request.POST.get('proposicao_id')
        if not proposicao_id:
            return JsonResponse({'status': 'error', 'message': 'ID não fornecido'}, status=400)
        
        try:
            proposicao = ProcessoLegislativo.objects.get(id=proposicao_id)
            
            # Sincroniza sob demanda no momento em que é adicionado para acompanhar
            sync_processo_on_demand(proposicao)
            
            termo, created = TermoMonitorado.objects.get_or_create(
                palavra_chave=f"proposicao_{proposicao.id_externo}"
            )
            termo.users.add(request.user)
            termo.processos.add(proposicao)
            
            return JsonResponse({'status': 'success'})
        except ProcessoLegislativo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Proposição não encontrada'}, status=404)

class ToggleFavoritoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            proposicao_id = data.get('proposicao_id')
        except json.JSONDecodeError:
            proposicao_id = request.POST.get('proposicao_id')

        if not proposicao_id:
            return JsonResponse({'status': 'error', 'message': 'ID não fornecido'}, status=400)
        
        try:
            proposicao = ProcessoLegislativo.objects.get(id=proposicao_id)
            
            # Verifica se o usuário já monitora sob qualquer termo
            termos_existentes = TermoMonitorado.objects.filter(
                users=request.user,
                processos=proposicao
            )
            
            if termos_existentes.exists():
                # Se já monitora, remove de todos os termos vinculados a ele
                for termo in termos_existentes:
                    termo.processos.remove(proposicao)
                    # Opcional: Se o termo ficar sem processos e sem outros usuários (exceto palavra_chave padrão), poderia deletar, mas remove() já basta.
                return JsonResponse({'status': 'success', 'action': 'removed'})
            else:
                # Se não monitora, adiciona a "meus_favoritos"
                termo, created = TermoMonitorado.objects.get_or_create(
                    palavra_chave="meus_favoritos"
                )
                termo.users.add(request.user)
                termo.processos.add(proposicao)
                sync_processo_on_demand(proposicao)
                return JsonResponse({'status': 'success', 'action': 'added'})
        except ProcessoLegislativo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Proposição não encontrada'}, status=404)

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")