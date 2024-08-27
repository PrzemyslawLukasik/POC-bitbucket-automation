import logging
from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass
class CreateBranchLocators:
    def __init__(self, page: Page):
        self.page = page

    def new_branch_name_locator(self) -> Locator:
        return self.page.locator('input[name="branchName"]')

    def create_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Create", exact=True)


class CreateBranchPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = CreateBranchLocators(self.page)

    def fill_in_new_branch_name(self, name: str) -> None:
        self.locators.new_branch_name_locator().wait_for(state="visible")
        self.locators.new_branch_name_locator().fill(name)

    def click_on_create_button(self) -> None:
        self.locators.create_button_locator().click()
