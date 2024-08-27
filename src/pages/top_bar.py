from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect


@dataclass
class TopBarLocators:
    def __init__(self, page: Page):
        self.page = page

    def your_work_link_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Your work")

    def pull_requests_link_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Pull requests")

    def repositories_link_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Repositories")

    def create_button_locator(self) -> Locator:
        return self.page.get_by_test_id("create-button")

    def repository_create_item_locator(self) -> Locator:
        return self.page.get_by_test_id("repository-create-item")


class TopBarPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = TopBarLocators(self.page)

    def click_on_your_work_item(self) -> None:
        self.locators.your_work_link_locator().click()
        self.page.wait_for_load_state("load", timeout=10000)

    def click_on_pull_requests_item(self) -> None:
        self.locators.pull_requests_link_locator().click()
        self.page.wait_for_load_state("load", timeout=10000)

    def click_on_repositories_item(self) -> None:
        self.locators.repositories_link_locator().click()
        self.page.wait_for_load_state("load", timeout=10000)

    def click_on_create_button(self) -> None:
        self.locators.create_button_locator().click()
        self.page.wait_for_load_state("load", timeout=10000)

    def click_on_repository_create_item(self) -> None:
        self.locators.repository_create_item_locator().click()
        self.page.wait_for_load_state("load", timeout=10000)

    def create_button_visible(self) -> bool:
        return (
            True
            if self.locators.repository_create_item_locator().is_visible(timeout=10000)
            else False
        )
