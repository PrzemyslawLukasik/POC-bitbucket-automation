import logging
from dataclasses import dataclass

from playwright.sync_api import Locator, Page

page_log = logging.getLogger("PAGE")


@dataclass
class FileEditLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def source_of_file_locator(self) -> Locator:
        return self.page.locator(selector=".CodeMirror-lines")

    def commit_button_locator(self) -> Locator:
        return self.page.get_by_role(role="button", name="Commit")


class FileEditPo:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.locators = FileEditLocators(self.page)

    def is_file_source_visible(self) -> bool:
        locator = self.locators.source_of_file_locator().wait_for(
            state="attached", timeout=10000
        )
        return True if locator else False

    def click_on_commit_button(self) -> None:
        page_log.info("Click on commit button")
        self.locators.commit_button_locator().click()

    def get_file_source(self) -> str:
        page_log.info("Geting file source")
        file_source = self.locators.source_of_file_locator()
        page_log.debug(f"File source:\n{file_source}")
        return file_source.all_inner_texts()

    def type_in_source_file(self, text: str) -> None:
        self.locators.source_of_file_locator().page.keyboard.type(text)

    def edit_source_of_file(self, text: str) -> str:
        self.locators.source_of_file_locator().wait_for(state="visible", timeout=10000)
        new_content = text
        self.type_in_source_file(new_content)
        return new_content
