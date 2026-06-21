from playwright.sync_api import expect
from Usuarios.models import User
from Processos.models import ProcessoLegislativo, TermoMonitorado
import pytest

@pytest.mark.django_db(transaction=True)
def test_favoritos_render_and_filters(page, live_server):
    # Setup
    user = User.objects.create_user(username="test_fav", password="123")
    
    # Criar proposição favoritada
    processo = ProcessoLegislativo.objects.create(
        id_externo="111",
        origem_camara_ou_senado="Camara",
        numero="10",
        ano="2024",
        tipo_proposicao="PL",
        ementa="Ementa de teste favoritos"
    )
    
    termo = TermoMonitorado.objects.create(palavra_chave="proposicao_111")
    termo.processos.add(processo)
    termo.users.add(user)

    # Login
    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', 'test_fav')
    page.fill('input[name="password"]', '123')
    page.click('button[type="submit"]')
    
    # Go to Favoritos
    page.goto(f"{live_server.url}/favoritos/")
    
    # Verifica abas de filtros
    expect(page.locator("text=Em Tramitação Normal").first).to_be_visible()
    expect(page.locator("text=Estagnadas (Atrasadas)").first).to_be_visible()
    
    # Verifica cards com Dias em Trâmite
    expect(page.locator("text=Dias em Trâmite")).to_be_visible()
    expect(page.locator("text=PL 10/2024")).to_be_visible()
    expect(page.locator("text=Ementa de teste favoritos")).to_be_visible()
