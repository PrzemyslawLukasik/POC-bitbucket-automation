import logging
import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from src.pages.base_page import BasePage
from src.pages.repository.repository_page.branches_po import BranchesPo
from src.pages.repository.repository_page.commit_popup_po import CommitPopupPo
from src.pages.repository.repository_page.file_edit_po import FileEditPo
from src.pages.repository.repository_page.file_view_po import FileViewPo
from src.pages.repository.repository_page.repository_sidebar_po import (
    RepositorySidebarPo,
)
from src.pages.repository.repository_page.source_po import RepositorySourcePo

page_log = logging.getLogger("PAGE")


@dataclass
class RepositoryPageLocators:
    def __init__(self, page: Page):
        self.page = page

    def repository_header_locator(self) -> Locator:
        return self.page.get_by_text("Let's put some bits in your").wait_for()

    def create_readme_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Create a README")


class RepositoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.locators = RepositoryPageLocators(self.page)
        self.sidebar = RepositorySidebarPo(self.page)
        self.file_edit = FileEditPo(self.page)
        self.commit_popup = CommitPopupPo(self.page)
        self.file_view = FileViewPo(self.page)
        self.source_view = RepositorySourcePo(self.page)
        self.branches_view = BranchesPo(self.page)

    def create_readme_click(self) -> None:
        self.locators.create_readme_locator().click()

    def create_default_readme_file(self) -> None:
        self.create_readme_click()
        self.file_edit.click_on_commit_button()
        self.commit_popup.is_commit_header_visible()
        self.commit_popup.enter_commit_message("ADD: README.md file")
        self.commit_popup.click_on_commit_button()
        self.source_view.is_article_loaded()
        readme_content = self.source_view.get_readme_article_content()
        page_log.debug(f"Readme content: {readme_content}")
        assert "README" in readme_content[0], "Readme file content missmatch"

    def edit_readme_file_content(self, text: str) -> str:
        self.source_view.click_on_selected_file("README.md")
        self.file_view.click_on_edit_button()
        self.file_edit.edit_source_of_file(text)
        self.file_edit.click_on_commit_button()
        self.commit_popup.edit_commit_message("Commit edited" + text)
        self.commit_popup.click_on_commit_button()
        self.sidebar.locators.source_link_locator().first.click()
        self.source_view.locators.article_locator().wait_for(
            state="visible", timeout=5000
        )
        article = self.source_view.get_readme_article_content()
        page_log.debug(f"article:\n {article}")
