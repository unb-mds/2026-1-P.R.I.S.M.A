import pytest
from playwright.sync_api import expect

@pytest.mark.django_db(transaction=True)
def test_sanity_check_home(page, live_server):
    from Usuarios.models import User
    user = User.objects.create_user(username="sanity_tester", password="123")

    page.goto(f"{live_server.url}/accounts/login/")
    page.fill('input[name="username"]', 'sanity_tester')
    page.fill('input[name="password"]', '123')
    page.click('button[type="submit"]')

    # Verifica o título da página ou a presença de 'P.R.I.S.M.A' no body
    import re
    expect(page).to_have_title(re.compile(r"P\.R\.I\.S\.M\.A"), timeout=5000)
    # Verifica se os novos elementos da sidebar estão presentes
    expect(page.locator("text=Monitor de Prazos")).to_be_visible()
    expect(page.locator("text=Configurações")).to_be_visible()
