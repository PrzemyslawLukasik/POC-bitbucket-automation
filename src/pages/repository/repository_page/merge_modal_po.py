import logging
import re
from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from src.pages.repository.repository_page.create_branch_po import CreateBranchPo


@dataclass
class MergeModalLocators:
    def __init__(self, page: Page):
        self.page = page

    def commit_message_locator(self) -> Locator:
        return self.page.get_by_label("Commit message")

    def merge_button_locator(self) -> Locator:
        return (
            self.page.locator("div")
            .filter(has_text=re.compile(r"^MergeCancel$"))
            .locator("button")
        )


class MergeModalPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = MergeModalLocators(self.page)

    def enter_merge_message(self, message: str) -> None:
        self.locators.commit_message_locator().wait_for(state="visible")
        self.locators.commit_message_locator().clear()
        self.locators.commit_message_locator().fill(message)

    def click_on_merge_button(self) -> None:
        self.locators.merge_button_locator().wait_for(state="visible")
        self.locators.merge_button_locator().click()
