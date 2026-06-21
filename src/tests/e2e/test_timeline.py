import pytest
from playwright.sync_api import expect
from django.contrib.auth import get_user_model
from Processos.models import ProcessoLegislativo, Movimentacao
from django.utils import timezone

User = get_user_model()

@pytest.fixture
def test_user(db):
    user, created = User.objects.get_or_create(
        username="testuser", 
        defaults={"email": "testuser@example.com"}
    )
    if created:
        user.set_password("testpassword")
        user.save()
    return user

@pytest.fixture
def mock_proposicao(db):
    processo, _ = ProcessoLegislativo.objects.get_or_create(
        id_externo="123456",
        defaults={
            "origem_camara_ou_senado": "Camara",
            "numero": "1234",
            "ano": "2023",
            "ementa": "Testa a criação de uma linha do tempo",
            "tipo_proposicao": "PL",
            "status_atual": "Em Tramitação"
        }
    )
    
    Movimentacao.objects.create(
        processo=processo,
        data_evento=timezone.now(),
        descricao="Enviado para a comissão especial de testes",
        comissao_atual="Comissão de Testes"
    )
    
    return processo

@pytest.mark.django_db
def test_timeline_historico_tramitacao_e_acompanhamento(page, live_server, test_user, mock_proposicao):
    """
    Testa se o fluxo de acompanhar uma proposição pelo modal funciona
    e se a página exibe corretamente a timeline (histórico de tramitação).
    """
    # 1. Login
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testpassword")
    page.click('button[type="submit"]')
    
    # 2. Navegar para proposições
    page.goto(f"{live_server.url}/proposicoes/")
    
    # 3. Verificar que a proposição não aparece inicialmente
    expect(page.locator("body")).not_to_contain_text("PL 1234/2023")
    
    # 4. Abrir o modal de Acompanhar
    page.click('button:has-text("+ Acompanhar Nova Proposição")')
    expect(page.locator("#searchModal")).to_be_visible()
    
    # 5. Buscar pela proposição
    page.fill('#searchInput', '1234')
    
    # 6. Esperar o resultado aparecer e clicar em Acompanhar
    expect(page.locator("#searchResults")).to_contain_text("Testa a criação de uma linha do tempo", timeout=3000)
    page.click('#searchResults button:has-text("Acompanhar")')
    
    # 7. A página recarrega e a proposição deve aparecer com a timeline
    expect(page.locator("body")).to_contain_text("PL 1234/2023", timeout=3000)
    expect(page.locator("body")).to_contain_text("Testa a criação de uma linha do tempo")
    expect(page.locator("body")).to_contain_text("Linha do Tempo Legislativa: PL 1234/2023")
    expect(page.locator("body")).to_contain_text("Comissão de Testes")
    expect(page.locator("body")).to_contain_text("Enviado para a comissão especial de testes")
    
    # 8. Verificar as colunas de tracking de Tempo / SLA
    expect(page.locator("body")).to_contain_text("0d total")
    expect(page.locator("body")).to_contain_text("0d estagnado")
