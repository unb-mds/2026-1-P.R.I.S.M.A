from playwright.sync_api import expect
from Usuarios.models import Notificacao, User
from Processos.models import ProcessoLegislativo
import pytest

@pytest.mark.django_db(transaction=True)
def test_alertas_render_and_empty_state(page, live_server):
    # Cria um usuário e faz login
    user = User.objects.create_user(username="tester", password="123")
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', 'tester')
    page.fill('input[name="password"]', '123')
    page.click('button[type="submit"]')
    
    # Navega para alertas
    page.goto(f"{live_server.url}/alertas/")
    
    # Verifica estado vazio
    expect(page.locator("text=Nenhuma notificação encontrada.")).to_be_visible()

@pytest.mark.django_db(transaction=True)
def test_alertas_render_notifications(page, live_server):
    # Cria usuário e dados
    user = User.objects.create_user(username="tester2", password="123")
    processo = ProcessoLegislativo.objects.create(
        id_externo="111",
        origem_camara_ou_senado="Camara",
        numero="10",
        ano="2024",
        tipo_proposicao="PL"
    )
    Notificacao.objects.create(
        user=user,
        processo=processo,
        tipo="ESTAGNACAO",
        mensagem="Processo estagnado"
    )

    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', 'tester2')
    page.fill('input[name="password"]', '123')
    page.click('button[type="submit"]')
    
    page.goto(f"{live_server.url}/alertas/")
    
    # Verifica se a notificação aparece
    expect(page.locator("text=Alerta de Estagnação")).to_be_visible()
    expect(page.locator("text=PL 10/2024")).to_be_visible()
    expect(page.locator("text=Processo estagnado")).to_be_visible()
