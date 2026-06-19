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
    # Ou então, verificar se há um H1 com P.R.I.S.M.A
    # expect(page.locator("h1")).to_contain_text("P.R.I.S.M.A")
