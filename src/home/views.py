from django.views.generic import TemplateView, CreateView, ListView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import models

from .forms import SignUpForm
from Processos.models import ProcessoLegislativo, TermoMonitorado


class DashboardView(TemplateView):
    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "dashboard"
        return context


class ProposicoesView(LoginRequiredMixin, ListView):
    template_name = "home/proposicoes.html"
    model = ProcessoLegislativo
    context_object_name = "proposicoes"

    def get_queryset(self):
        return ProcessoLegislativo.objects.filter(
            termos_monitorados__users=self.request.user
        ).distinct().prefetch_related('movimentacoes')

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


class FavoritosView(LoginRequiredMixin, TemplateView):
    template_name = "home/favoritos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "favoritos"
        return context


class AlertasView(LoginRequiredMixin, TemplateView):
    template_name = "home/alertas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "alertas"
        return context


class UsuarioView(LoginRequiredMixin, TemplateView):
    template_name = "home/usuario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "usuario"
        return context

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