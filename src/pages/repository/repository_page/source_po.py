import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage
from src.pages.repository.repository_page.repository_sidebar_po import (
    RepositorySidebarPo,
)


@dataclass
class RepositorySourceLocators:
    def __init__(self, page: Page):
        self.page = page

    def branch_selector_locator(self) -> Locator:
        return self.page.get_by_test_id("ref-selector-trigger")

    def branch_filter_locator(self) -> Locator:
        return self.page.get_by_placeholder("Filter branches")

    def branch_select_locator(self, branch_name: str) -> Locator:
        locator = self.page.get_by_role("link", name=branch_name)
        return locator

    def search_entity_selector_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Files")

    def search_textbox_locator(self) -> Locator:
        return self.page.get_by_placeholder("Filter files")

    def repo_item_locator(self, type: str, file_name: str) -> Locator:
        name = f"{type}, {file_name}"
        return self.page.get_by_role("link", name=f"{name}")

    def article_locator(self) -> Locator:
        return self.page.get_by_role("article")

    def edit_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Edit")

    def repo_actions_menu_locator(self) -> Locator:
        return self.page.get_by_test_id("repo-actions-menu--trigger")

    def compare_branches_link_locator(self) -> Locator:
        return self.page.get_by_role("menuitem", name="Compare commits, branches or")


class RepositorySourcePo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = RepositorySourceLocators(self.page)

    def get_readme_article_content(self) -> str:
        self.locators.article_locator().wait_for(state="visible", timeout=10000)
        return self.locators.article_locator().all_text_contents()

    def verify_that_readme_include(self, text: str) -> bool:
        article = self.get_readme_article_content()
        assert text in article[0], "Readme not updated"

    def click_on_edit_button(self) -> None:
        self.locators.edit_button_locator().click()

    def click_on_selected_file(self, file_name: str) -> None:
        self.locators.repo_item_locator("file", file_name).click()

    def is_article_loaded(self) -> None:
        self.locators.article_locator().wait_for(state="visible", timeout=10000)

    def change_branch_to(self, branch_name: str) -> None:
        self.locators.branch_selector_locator().wait_for(state="visible")
        self.locators.branch_selector_locator().click()
        self.locators.branch_filter_locator().wait_for(state="visible")
        self.locators.branch_filter_locator().fill(branch_name)
        self.locators.branch_select_locator(branch_name).click()

    def click_on_menu_button(self) -> None:
        self.locators.repo_actions_menu_locator().click()

    def compare_branches(self) -> None:
        self.click_on_menu_button()
        self.locators.compare_branches_link_locator().wait_for(state="visible")
        self.locators.compare_branches_link_locator().click()
