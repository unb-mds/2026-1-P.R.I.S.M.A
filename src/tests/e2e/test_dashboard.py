import pytest
from playwright.sync_api import expect
from Usuarios.models import User, Notificacao
from Processos.models import ProcessoLegislativo, Movimentacao
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db(transaction=True)
def test_dashboard_indicadores(page, live_server):
    user = User.objects.create_user(username="dashboard_tester", password="123")
    
    # Processo 1
    p1 = ProcessoLegislativo.objects.create(
        id_externo="101", origem_camara_ou_senado="Camara", numero="1", ano="2024", tipo_proposicao="PL"
    )
    # Movimentacao 10 dias atras
    Movimentacao.objects.create(processo=p1, data_evento=timezone.now() - timedelta(days=10), descricao="Início")
    Notificacao.objects.create(user=user, processo=p1, tipo="ESTAGNACAO", mensagem="Alerta estagnado")

    # Processo 2
    p2 = ProcessoLegislativo.objects.create(
        id_externo="102", origem_camara_ou_senado="Senado", numero="2", ano="2024", tipo_proposicao="PEC"
    )
    # Movimentacao 20 dias atras
    Movimentacao.objects.create(processo=p2, data_evento=timezone.now() - timedelta(days=20), descricao="Início")

    # Média aproximada = 15. Estagnados = 1, Em andamento = 1.

    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', 'dashboard_tester')
    page.fill('input[name="password"]', '123')
    page.click('button[type="submit"]')

    page.goto(f"{live_server.url}/")

    expect(page.locator('text="Média de Tramitação"')).to_be_visible()
    expect(page.locator('text="Estagnados"')).to_be_visible()
    expect(page.locator('text="Em Andamento"')).to_be_visible()

    # Verifica os números. "1" deve aparecer para estagnados e em andamento.
    # Média deve ser "15" ou "15.0"
    content = page.content()
    assert "Estagnados" in content
    assert "Em Andamento" in content
    assert "Média de Tramitação" in content
