import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect
from slugify import slugify

from src.pages.base_page import BasePage


@dataclass
class RepositoriesListLocators:
    def __init__(self, page: Page):
        self.page = page

    def repositories_header_locator(self) -> Locator:
        return self.page.get_by_test_id("Content").get_by_text(
            "Repositories", exact=True
        )

    def repositories_search_field_locator(self) -> Locator:
        return self.page.get_by_placeholder("Search repositories")

    def repository_link_locator(self, repository_name: str) -> Locator:
        locator = self.page.get_by_label(repository_name)
        locator.wait_for()
        return locator


class RepositoriesListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = os.environ["APP_URL"] + "/workspace/repositories"
        self.locators = RepositoriesListLocators(self.page)

    def is_repositories_header_visible(self) -> bool:
        return (
            True if self.locators.repositories_header_locator().is_visible() else False
        )

    def is_the_repository_visible(self, repository_name) -> bool:
        self.locators.repository_link_locator(repository_name).wait_for(
            state="visible", timeout=10000
        )
        return True if self.locators.repository_link_locator(repository_name) else False

    def search_for_repository(self, repository_name) -> bool:
        repository_name_slug = slugify(repository_name)
        self.locators.repositories_search_field_locator().fill(repository_name_slug)
        return self.is_the_repository_visible(repository_name)

    def select_repository(self, repository_name: str) -> None:
        self.search_for_repository(repository_name)
        self.locators.repository_link_locator(repository_name).click()
