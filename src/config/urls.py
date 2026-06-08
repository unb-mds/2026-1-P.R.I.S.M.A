from django.contrib import admin
from django.urls import path
from home.views import DashboardView, ProposicoesView, VotacoesView
from home.views import FavoritosView, AlertasView, UsuarioView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", DashboardView.as_view(), name="dashboard"),
    path("proposicoes/", ProposicoesView.as_view(), name="proposicoes"),
    path("votacoes/", VotacoesView.as_view(), name="votacoes"),
    path("favoritos/", FavoritosView.as_view(), name="favoritos"),
    path("alertas/", AlertasView.as_view(), name="alertas"),
    path("usuario/", UsuarioView.as_view(), name="usuario"),
]
