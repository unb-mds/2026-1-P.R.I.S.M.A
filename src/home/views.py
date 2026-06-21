from django.views.generic import TemplateView, CreateView, ListView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Avg, Min, Max, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractDay
from django.utils import timezone
import datetime
from Usuarios.models import Notificacao, UserProfile

from .forms import SignUpForm
from Processos.models import ProcessoLegislativo, TermoMonitorado
from Processos.services import sync_processo_on_demand


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


class ProposicoesView(LoginRequiredMixin, ListView):
    template_name = "home/proposicoes.html"
    model = ProcessoLegislativo
    context_object_name = "proposicoes"

    def get_queryset(self):
        qs = ProcessoLegislativo.objects.filter(
            termos_monitorados__users=self.request.user
        ).distinct().prefetch_related('movimentacoes')
        
        # Sincroniza sob demanda quando o usuário acessa a página
        for processo in qs:
            sync_processo_on_demand(processo)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "proposicoes"
        return context


class VotacoesView(LoginRequiredMixin, TemplateView):
    template_name = "home/votacoes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "votacoes"
        return context


class FavoritosView(LoginRequiredMixin, ListView):
    template_name = "home/favoritos.html"
    context_object_name = "favoritos"

    def get_queryset(self):
        qs = ProcessoLegislativo.objects.filter(
            termos_monitorados__users=self.request.user
        ).distinct().prefetch_related('movimentacoes')
        
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
        ).distinct().annotate(ultima_mov=Max('movimentacoes__data_evento'))
        
        limite = timezone.now() - datetime.timedelta(days=30)
        
        context["total_count"] = base_qs.count()
        context["normal_count"] = base_qs.filter(ultima_mov__gte=limite).count()
        context["estagnadas_count"] = base_qs.filter(ultima_mov__lt=limite).count()
        context["urgencia_count"] = base_qs.filter(notificacoes__lida=False).distinct().count()
        
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

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")