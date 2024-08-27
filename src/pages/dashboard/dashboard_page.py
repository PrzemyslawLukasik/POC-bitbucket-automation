from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from src.pages.base_page import BasePage
from src.pages.top_bar import TopBarPo


@dataclass
class DashboardLocators:
    def __init__(self, page: Page):
        self.page = page

    def welcome_text_locator(self) -> Locator:
        return self.page.get_by_text("Welcome to Bitbucket!")

    def repository_link_locator(self, repository_name: str) -> Locator:
        self.page.get_by_role("link", name=repository_name).wait_for()
        return self.page.get_by_role("link", name=repository_name)


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = DashboardLocators(self.page)
        self.top_bar = TopBarPo(self.page)

    def is_repository_visible(self, repository_name) -> bool:
        self.locators.repository_link_locator(repository_name).wait_for(
            state="visible", timeout=10000
        )
        return True if self.locators.repository_link_locator(repository_name) else False
