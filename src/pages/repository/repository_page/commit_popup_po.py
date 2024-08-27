import re
from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass
class CommitPopupLocators:
    def __init__(self, page: Page):
        self.page = page

    def commit_header_locator(self) -> Locator:
        return self.page.get_by_text("Commit changes")

    def commit_textfield_locator(self) -> Locator:
        return self.page.get_by_label("Commit message")

    def commit_button_locator(self) -> Locator:
        return (
            self.page.locator("div")
            .filter(has_text=re.compile(r"^CommitCancel$"))
            .locator("button")
        )

    def cancel_link_locator(self) -> Locator:
        return self.page.get_by_text("Cancel")


class CommitPopupPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = CommitPopupLocators(self.page)

    def is_commit_header_visible(self) -> bool:
        self.locators.commit_header_locator().wait_for(state="visible", timeout=10000)
        return True if self.locators.commit_header_locator() else False

    def clear_text_field(self) -> None:
        self.locators.commit_textfield_locator().clear()

    def enter_commit_message(self, message: str) -> None:
        self.locators.commit_textfield_locator().fill(message)

    def get_commit_message(self) -> str:
        return self.locators.commit_textfield_locator().all_inner_texts()

    def edit_commit_message(self, add_text: str) -> str:
        message = self.get_commit_message()
        self.enter_commit_message(f"{message} {add_text}")
        edited_message = self.get_commit_message()
        return edited_message

    def click_on_commit_button(self) -> None:
        self.locators.commit_button_locator().click()

    def click_on_cancel_link(self) -> None:
        self.locators.cancel_link_locator().click()
