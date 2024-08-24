import os
import pytest
import time

from playwright.sync_api import Page

from src.pages.login_page import LoginPage




def test_browser(page: Page) -> None:
    # page.goto("https://bitbucket.org/auto-test-pl")
    time.sleep(10)
    print(os.environ["USERNAME"])
    assert True