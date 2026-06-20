import pytest
from playwright.sync_api import expect
from django.contrib.auth import get_user_model
from Processos.models import ProcessoLegislativo, Movimentacao
from django.utils import timezone
import datetime

User = get_user_model()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user

@pytest.fixture
def mock_proposicao(db):
    processo = ProcessoLegislativo.objects.create(
        id_externo="123456",
        origem_camara_ou_senado="Camara",
        numero="1234",
        ano="2023",
        ementa="Testa a criação de uma linha do tempo",
        tipo_proposicao="PL",
        status_atual="Em Tramitação"
    )
    
    Movimentacao.objects.create(
        processo=processo,
        data_evento=timezone.now(),
        descricao="Enviado para a comissão especial de testes",
        comissao_atual="Comissão de Testes"
    )
    
    return processo

@pytest.mark.django_db
def test_timeline_historico_tramitacao(page, live_server, test_user, mock_proposicao):
    """
    Testa se a página de proposições exibe corretamente a timeline (histórico de tramitação)
    da proposição cadastrada no banco.
    """
    # 1. Login
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testpassword")
    page.click('button[type="submit"]')
    
    # 2. Navegar para proposições
    page.goto(f"{live_server.url}/proposicoes/")
    
    # 3. Verificar se a proposição aparece
    expect(page.locator("body")).to_contain_text("PL 1234/2023")
    expect(page.locator("body")).to_contain_text("Testa a criação de uma linha do tempo")
    
    # 4. Verificar se a linha do tempo e a movimentação aparecem
    expect(page.locator("body")).to_contain_text("Linha do Tempo Legislativa: PL 1234/2023")
    expect(page.locator("body")).to_contain_text("Comissão de Testes")
    expect(page.locator("body")).to_contain_text("Enviado para a comissão especial de testes")
