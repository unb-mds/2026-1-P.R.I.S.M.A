from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import SignUpForm


class DashboardView(TemplateView):
    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "dashboard"
        return context


class ProposicoesView(LoginRequiredMixin, TemplateView):
    template_name = "home/proposicoes.html"

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

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")