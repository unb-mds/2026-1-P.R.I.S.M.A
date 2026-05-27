from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'home/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'dashboard'
        return context


class ProposicoesView(TemplateView):
    template_name = 'home/proposicoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'proposicoes'
        return context


class VotacoesView(TemplateView):
    template_name = 'home/votacoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'votacoes'
        return context


class FavoritosView(TemplateView):
    template_name = 'home/favoritos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'favoritos'
        return context


class AlertasView(TemplateView):
    template_name = 'home/alertas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'alertas'
        return context


class UsuarioView(TemplateView):
    template_name = 'home/usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'usuario'
        return context
