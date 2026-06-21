from playwright.sync_api import expect
from Usuarios.models import User, UserProfile
import pytest

@pytest.mark.django_db(transaction=True)
def test_configuracoes_salvar(page, live_server):
    # Setup
    user = User.objects.create_user(username="test_conf", password="123")
    
    # Login
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', 'test_conf')
    page.fill('input[name="password"]', '123')
    page.click('button[type="submit"]')
    
    # Navegar para as configurações (Usuário)
    page.goto(f"{live_server.url}/usuario/")
    
    # Verifica a renderização do form
    expect(page.locator("text=Alertas de Estagnação")).to_be_visible()
    
    # Altera valor
    page.fill('input[name="dias_limite_estagnacao"]', '45')
    
    # Desmarca receber novas movimentacoes
    page.click('input[name="receber_alertas_novas_movimentacoes"] + div')
    
    # Submit
    page.click('button:has-text("Salvar Configurações")')
    
    # Verifica mensagem de sucesso
    expect(page.locator("text=Configurações Salvas!")).to_be_visible()
    
    # Verifica se os valores estão no form
    expect(page.locator('input[name="dias_limite_estagnacao"]')).to_have_value('45')
    
    # Verifica no banco de dados
    user.refresh_from_db()
    profile = user.profile
    assert profile.dias_limite_estagnacao == 45
    assert profile.receber_alertas_novas_movimentacoes is False
