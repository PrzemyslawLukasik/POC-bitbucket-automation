from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass
class FileViewLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def view_type_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Source", exact=True)

    def branch_selector_locator(self) -> Locator:
        return self.page.get_by_test_id("ref-selector-trigger")

    def edit_link_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Edit")


class FileViewPo:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.locators = FileViewLocators(self.page)

    def click_on_commit_button(self) -> None:
        self.locators.edit_link_locator().click()

    def click_on_edit_button(self) -> None:
        self.locators.edit_link_locator().click()
