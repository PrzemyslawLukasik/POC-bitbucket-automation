import time
from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass
class RepositorySidebarLocators:
    def __init__(self, page: Page):
        self.page = page

    def repository_name_link_locator(self, repository_name) -> Locator:
        self.page.get_by_role("link", name=repository_name).wait_for()
        return self.page.get_by_role("link", name=repository_name)

    def source_link_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Source").first

    def branches_link_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Branches")


class RepositorySidebarPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = RepositorySidebarLocators(self.page)

    def is_repository_name_visible(self, repository_name: str) -> bool:
        return (
            True
            if self.locators.repository_name_link_locator(
                repository_name=repository_name
            )
            else False
        )

    def click_on_source_link(self) -> None:
        self.locators.source_link_locator().wait_for(state="visible", timeout=10000)
        self.locators.source_link_locator().click()

    def click_on_branches_link(self) -> None:
        self.locators.branches_link_locator().click()
