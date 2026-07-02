import pytest
from playwright.sync_api import expect
from django.contrib.auth import get_user_model
from Processos.models import ProcessoLegislativo

User = get_user_model()

@pytest.fixture
def test_user(db):
    user, created = User.objects.get_or_create(
        username="testuser_ia", 
        defaults={"email": "ia@example.com"}
    )
    if created:
        user.set_password("testpassword")
        user.save()
    return user

@pytest.fixture
def processo_com_ia(db):
    processo, _ = ProcessoLegislativo.objects.get_or_create(
        id_externo="8888888",
        defaults={
            "origem_camara_ou_senado": "Camara",
            "numero": "8888888",
            "ano": "2024",
            "ementa": "Ementa teste IA",
            "tipo_proposicao": "PL",
            "status_atual": "Em Tramitação",
            "estimativa_dias_conclusao": 45,
            "porcentagem_conclusao": 60.5
        }
    )
    return processo

@pytest.fixture
def processo_sem_ia(db):
    processo, _ = ProcessoLegislativo.objects.get_or_create(
        id_externo="7777777",
        defaults={
            "origem_camara_ou_senado": "Camara",
            "numero": "7777777",
            "ano": "2024",
            "ementa": "Ementa teste SEM IA",
            "tipo_proposicao": "PL",
            "status_atual": "Em Tramitação",
            "estimativa_dias_conclusao": None,
            "porcentagem_conclusao": None
        }
    )
    return processo

@pytest.mark.django_db
def test_previsao_ia_sucesso(page, live_server, test_user, processo_com_ia):
    # 1. Login
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', "testuser_ia")
    page.fill('input[name="password"]', "testpassword")
    page.click('button[type="submit"]')
    
    # 2. Navegar para detalhes do processo com IA
    page.goto(f"{live_server.url}/processos/{processo_com_ia.id}/")
    
    # 3. Validar exibição da barra premium e badge IA
    expect(page.locator("body")).to_contain_text("Previsão IA", timeout=3000)
    expect(page.locator("body")).to_contain_text("~45 dias")
    expect(page.locator("body")).to_contain_text("61%")
    expect(page.locator("text=Estimativa indisponível")).not_to_be_visible()

@pytest.mark.django_db
def test_previsao_ia_falha(page, live_server, test_user, processo_sem_ia):
    # 1. Login
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', "testuser_ia")
    page.fill('input[name="password"]', "testpassword")
    page.click('button[type="submit"]')
    
    # 2. Navegar para detalhes do processo SEM IA
    page.goto(f"{live_server.url}/processos/{processo_sem_ia.id}/")
    
    # 3. Validar exibição do Failsafe
    expect(page.locator("text=Estimativa indisponível")).to_be_visible(timeout=3000)
    # A barra premium não deve estar visível
    expect(page.locator("text=Previsão de Conclusão")).not_to_be_visible()
