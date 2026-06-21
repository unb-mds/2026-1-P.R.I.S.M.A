import pytest
from playwright.sync_api import expect
from django.contrib.auth import get_user_model
from Processos.models import ProcessoLegislativo, Movimentacao
from django.utils import timezone
from unittest.mock import patch

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
        id_externo="9999999",
        defaults={
            "origem_camara_ou_senado": "Camara",
            "numero": "9999999",
            "ano": "2023",
            "ementa": "Testa a criação de uma linha do tempo",
            "tipo_proposicao": "PL",
            "status_atual": "Em Tramitação"
        }
    )
    
    Movimentacao.objects.get_or_create(
        processo=processo,
        data_evento=timezone.now(),
        descricao="Enviado para a comissão especial de testes",
        defaults={"comissao_atual": "Comissão de Testes"}
    )
    
    return processo

@pytest.mark.django_db
def test_timeline_historico_tramitacao_e_acompanhamento(page, live_server, test_user, mock_proposicao):
    """
    Testa se o fluxo de acompanhar uma proposição pelo modal funciona
    e se a página exibe corretamente a timeline (histórico de tramitação).
    Usa mock para evitar bater na API real da Câmara/Senado durante os testes.
    """
    # Usamos o patch para simular a resposta da API de serviços
    with patch('Processos.services.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        # Simula que a API retornou vazio para não criar novas movimentações não esperadas, 
        # mantendo apenas a que foi criada no banco local via fixture mock_proposicao
        mock_get.return_value.json.return_value = {"dados": []}
        
        # 1. Login
        page.goto(f"{live_server.url}/accounts/login/")
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="password"]', "testpassword")
        page.click('button[type="submit"]')
        
        # 2. Navegar para processos
        page.goto(f"{live_server.url}/processos/")
        
        # 4. Abrir o modal de Acompanhar
        page.click('button:has-text("+ Acompanhar Novo Processo")')
        expect(page.locator("#searchModal")).to_be_visible()
        
        # 5. Buscar pela proposição com ID único
        page.fill('#searchInput', '9999999')
        
        # 6. Esperar o resultado aparecer e clicar em Acompanhar
        expect(page.locator("#searchResults")).to_contain_text("Testa a criação de uma linha do tempo", timeout=3000)
        page.click('#searchResults button:has-text("Acompanhar")')
        
        # 7. A página recarrega e a proposição deve aparecer
        expect(page.locator("body")).to_contain_text("PL 9999999/2023", timeout=3000)
        expect(page.locator("body")).to_contain_text("Testa a criação de uma linha do tempo")
        
        # 8. Clicar na proposição para ir para a página de Detalhes
        #    Aguarda o HTMX concluir as substituições de linha antes de clicar
        page.wait_for_load_state("networkidle", timeout=10000)
        page.locator("tr", has_text="PL 9999999/2023").click()
        
        # 9. Verificar a timeline na página de detalhes
        expect(page.locator("body")).to_contain_text("Histórico de Tramitação", timeout=3000)
        expect(page.locator("body")).to_contain_text("Comissão de Testes")
        expect(page.locator("body")).to_contain_text("Enviado para a comissão especial de testes")
        
        # 10. Testar o botão de Favorito na tela de detalhes
        # Como foi favoritado pelo modal, deve iniciar como "Acompanhando"
        expect(page.locator("#btnAcompanharText")).to_have_text("Acompanhando")
        
        # Clicar para remover dos favoritos
        page.click('#btnAcompanhar')
        expect(page.locator("#btnAcompanharText")).to_have_text("Acompanhar Favorito")
        
        # Clicar para favoritar novamente
        page.click('#btnAcompanhar')
        expect(page.locator("#btnAcompanharText")).to_have_text("Acompanhando")
        
        # 11. Verificar a Barra de Progresso Premium (Issue #15)
        expect(page.locator("text=Status Atual do Ciclo")).to_be_visible()
        expect(page.locator("body")).to_contain_text("10%") # Porque o status_atual é "Em Tramitação"
