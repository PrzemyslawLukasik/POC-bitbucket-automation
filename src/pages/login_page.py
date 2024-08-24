import os
import time
from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from src.pages.base_page import BasePage

from src.pages.fa_popup_po import FaPopupPo

@dataclass
class LoginPageLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def resource_not_found_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Resource not found")

    def resource_not_found_login_link_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Log in")

    def login_to_continue_header_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Log in to continue")

    def username_input_locator(self) -> Locator:
        return self.page.get_by_test_id("username")

    def continue_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Continue")
    
    def password_input_locator(self) -> Locator:
        return self.page.get_by_test_id("password")
    
    def log_in_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Log in")


@dataclass
class LoginPageStatics:

    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page=page)
        self.locators = LoginPageLocators(self.page)
        self.statics = LoginPageStatics()

        self.fa_popup = FaPopupPo(self.page)

        self.url = 'https://id.atlassian.com/login?application=bitbucket&continue=https%3A%2F%2Fbitbucket.org%2Faccount%2Fsignin%2F%3Fnext%3D%252F%26redirectCount%3D1'

    def resource_not_found_popup_visible(self) -> bool:
        return self.locators.resource_not_found_locator(
        ).is_visible(timeout=10)
    
    def login_to_continue_visible(self) -> bool:
        return self.locators.login_to_continue_header_locator(
        ).is_visible(timeout=10000)
    
    def password_input_visible(self) -> bool:
        return self.locators.password_input_locator().is_visible(timeout=10)
    
    def login(self) -> None:
        if self.resource_not_found_popup_visible():
            self.page.wait_for_load_state('load', timeout=10000)
            self.locators.resource_not_found_login_link_locator().click()
        else:
            print("NO RESOURCE NOT FOUND")
        self.page.wait_for_load_state('load', timeout=10000)
        self.login_to_continue_visible()
        self.locators.username_input_locator().is_visible()
        self.locators.username_input_locator().fill(self.statics.username)
        self.locators.continue_button_locator().click()
        self.locators.password_input_locator().wait_for()
        self.locators.password_input_locator().fill(self.statics.password)
        self.locators.log_in_button_locator().click()
        self.page.wait_for_load_state('load', timeout=10000)
        time.sleep(10)

