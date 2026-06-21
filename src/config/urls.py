from django.contrib import admin
from django.urls import path
from django.urls import include

from home.views import (
    DashboardView,
    ProposicoesView,
    VotacoesView,
    FavoritosView,
    AlertasView,
    UsuarioView,
    SignUpView,
    BuscarProposicaoView,
    AcompanharProposicaoView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "",
        DashboardView.as_view(),
        name="dashboard"
    ),

    path(
        "accounts/",
        include("django.contrib.auth.urls")
    ),

    path(
        "signup/",
        SignUpView.as_view(),
        name="signup"
    ),

    path(
        "proposicoes/",
        ProposicoesView.as_view(),
        name="proposicoes"
    ),

    path(
        "proposicoes/buscar/",
        BuscarProposicaoView.as_view(),
        name="buscar_proposicao"
    ),

    path(
        "proposicoes/acompanhar/",
        AcompanharProposicaoView.as_view(),
        name="acompanhar_proposicao"
    ),

    path(
        "votacoes/",
        VotacoesView.as_view(),
        name="votacoes"
    ),

    path(
        "favoritos/",
        FavoritosView.as_view(),
        name="favoritos"
    ),

    path(
        "alertas/",
        AlertasView.as_view(),
        name="alertas"
    ),

    path(
        "usuario/",
        UsuarioView.as_view(),
        name="usuario"
    ),
]