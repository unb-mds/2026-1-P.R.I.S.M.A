import pytest
from playwright.sync_api import expect

@pytest.mark.django_db
def test_sanity_check_home(page):
    """
    Testa se a página inicial está carregando corretamente e contém o título 'P.R.I.S.M.A'.
    Como a fixture 'page' já navega para a raiz (live_server.url), basta checar o conteúdo.
    """
    # Verifica o título da página ou a presença de 'P.R.I.S.M.A' no body
    import re
    expect(page).to_have_title(re.compile(r"P\.R\.I\.S\.M\.A"), timeout=5000)
    # Verifica se os novos elementos da sidebar estão presentes
    expect(page.locator("text=Monitor de Prazos")).to_be_visible()
    expect(page.locator("text=Configurações")).to_be_visible()
