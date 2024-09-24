import time

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    StorageState,
    sync_playwright,
)
from typing_extensions import Generator

from src.pages.login_page import LoginPage
from src.pages.top_bar import TopBarPo


@pytest.fixture(scope="session")
def admin_storage_state(browser: Browser) -> Generator[StorageState, None, None]:
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    top_bar = TopBarPo(page)
    login_page.visit()
    login_page.login()
    top_bar.locators.create_button_locator().wait_for()
    storage_state = context.storage_state()
    page.close()
    yield storage_state


# Fixture for the admin page with a new context
@pytest.fixture(scope="function")
def page(browser: Browser, admin_storage_state):
    context = browser.new_context(storage_state=admin_storage_state)
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    # Perform your login or setup for an admin user here
    # For example: page.goto("https://example.com/admin")
    yield page
    context.close()


# Fixture for a regular user page using the normal page
# @pytest.fixture
# def user_page(page):
#     # Perform any setup required for a regular user
#     # For example: page.goto("https://example.com/user")
#     return page


# @pytest.fixture(scope="function", autouse=True)
# def auth_check(browser, page: Page) -> BrowserContext:
#     login_page = LoginPage(page)
#     login_page.visit()
#     login_page.login()
#     # context = BrowserContext(browser).storage_state(path=".auth/auth_context.json")
#     return login_page
