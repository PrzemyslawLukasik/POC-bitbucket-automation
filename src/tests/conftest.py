import pytest

from playwright.sync_api import Page, BrowserContext
from src.pages.login_page import LoginPage

@pytest.fixture(scope="function", autouse=True)
def auth_check(browser, page: Page) -> BrowserContext:
    login_page = LoginPage(page)
    login_page.visit()
    login_page.login()
    # context = BrowserContext(browser).storage_state(path=".auth/auth_context.json")
    return login_page