import logging
from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from src.pages.repository.repository_page.create_branch_po import CreateBranchPo
from src.pages.repository.repository_page.merge_modal_po import MergeModalPo


@dataclass
class BranchesLocators:
    def __init__(self, page):
        self.page = page

    def branches_header_locator(self) -> Locator:
        return self.page.get_by_test_id("Content").get_by_text("Branches", exact=True)

    def create_branch_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Create branch")

    def compare_view_header_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Compare")

    def destination_branch_selector(self) -> Locator:
        return self.page.locator('data-fiels="dest"')

    def source_branch_selector(self) -> Locator:
        return self.page.locator('data-fiels="dest"')

    def branch_search_field_locator(self) -> Locator:
        return self.page.locator("#select2-drop").get_by_role("textbox")

    def branch_select_locator(self, branch_name: str) -> Locator:
        locator = self.page.get_by_title(branch_name)
        return locator

    def compare_button_locator(self) -> Locator:
        locator: Locator = self.page.get_by_role("button", name="Compare")
        return locator

    def create_a_pr_button_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Create pull request")

    def merge_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Merge")


class BranchesPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = BranchesLocators(self.page)
        self.create_branch_modal = CreateBranchPo(self.page)
        self.merge_modal = MergeModalPo(self.page)

    def branch_page_displayed(self) -> bool:
        self.locators.branches_header_locator().wait_for(state="visible")
        return True if self.locators.branches_header_locator().is_visible() else False

    def click_on_create_branch_button(self) -> None:
        self.locators.create_branch_button_locator().click()

    def create_new_branch(self, branch_name: str) -> None:
        self.branch_page_displayed()
        self.click_on_create_branch_button()
        self.create_branch_modal.fill_in_new_branch_name(branch_name)
        self.create_branch_modal.click_on_create_button()

    def click_on_dest_branch_selector(self) -> None:
        self.locators.destination_branch_selector().click()

    def click_on_source_branch_selector(self) -> None:
        self.locators.source_branch_selector().click()

    def search_for_branch(self, branch_name: str) -> None:
        self.locators.branch_search_field_locator().wait_for(state="visible")
        self.locators.branch_search_field_locator().fill(branch_name)

    def select_a_destination_branch(self, branch_name: str) -> None:
        self.locators.destination_branch_selector().wait_for(state="visible")
        self.click_on_dest_branch_selector()
        self.search_for_branch(branch_name)
        self.locators.branch_select_locator(branch_name)

    def select_a_source_branch(self, branch_name: str) -> None:
        self.locators.destination_branch_selector().wait_for(state="visible")
        self.click_on_dest_branch_selector()
        self.search_for_branch(branch_name)
        self.locators.branch_select_locator(branch_name)

    def click_on_compare_button(self) -> None:
        self.locators.compare_button_locator().wait_for(state="visible")
        self.locators.compare_button_locator().dblclick()

    def click_on_pr_button(self) -> None:
        self.locators.create_a_pr_button_locator().wait_for(state="visible")
        self.locators.create_a_pr_button_locator().click()

    def click_on_merge_button(self) -> None:
        self.locators.merge_button_locator().wait_for(state="visible", timeout=10000)
        self.locators.merge_button_locator().click()

    def merge_changes_to_master(self, branch_mame: str) -> None:
        self.click_on_merge_button()
        self.merge_modal.enter_merge_message(f"Merging: {branch_mame} to master")
        self.merge_modal.locators.merge_button_locator().wait_for(
            state="visible", timeout=10000
        )
        self.merge_modal.click_on_merge_button()
