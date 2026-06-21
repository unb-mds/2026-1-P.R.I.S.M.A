from django.contrib import admin
from django.urls import path
from django.urls import include

from home.views import (
    DashboardView,
    ProcessosView,
    FavoritosView,
    AlertasView,
    UsuarioView,
    SignUpView,
    BuscarProposicaoView,
    AcompanharProposicaoView,
    ProcessoDetailView,
    ToggleFavoritoView,
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
        "processos/",
        ProcessosView.as_view(),
        name="processos"
    ),

    path(
        "processos/buscar/",
        BuscarProposicaoView.as_view(),
        name="buscar_proposicao"
    ),

    path(
        "processos/<int:pk>/",
        ProcessoDetailView.as_view(),
        name="proposicao_detalhes"
    ),

    path(
        "processos/acompanhar/",
        AcompanharProposicaoView.as_view(),
        name="acompanhar_proposicao"
    ),

    path(
        "processos/toggle-favorito/",
        ToggleFavoritoView.as_view(),
        name="toggle_favorito"
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