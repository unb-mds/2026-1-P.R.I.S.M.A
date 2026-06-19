import os
import pytest

# Permite acesso ao banco de forma síncrona dentro de contexto async (como o Playwright)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Essa fixture instrui o Django LiveServer a disponibilizar sua URL para o Playwright
@pytest.fixture(scope="session")
def django_db_setup():
    """Configura o banco de dados do Django antes de rodar os testes."""
    pass

@pytest.fixture
def page(context, live_server):
    """
    Sobrescreve a fixture 'page' do Playwright para já abrir a aba
    na base_url do LiveServer do Django.
    """
    page = context.new_page()
    # live_server.url contém a URL em que o servidor de teste do Django subiu
    page.goto(live_server.url)
    return page
