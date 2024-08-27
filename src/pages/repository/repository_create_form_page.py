import logging
import time
from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from src.pages.base_page import BasePage
from src.pages.top_bar import TopBarPo

page_log = logging.getLogger("PAGE")


@dataclass
class CreateRepositoryLocators:
    def __init__(self, page: Page):
        self.page = page

    def heading_page_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Create a new repository")

    def project_name_input_locator(self) -> Locator:
        return self.page.locator("#id_project_name")

    def select_project_dropdown_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Select project")

    def select_project_locator(self, proj_name: str) -> Locator:
        self.page.get_by_text(proj_name).wait_for(timeout=10000, state="attached")
        page_log.info(
            f"Project found: {self.page.get_by_text(proj_name).all_inner_texts()}"
        )
        return self.page.get_by_text(proj_name)

    def selected_project_name_locator(self) -> Locator:
        return self.page.locator(".project-dropdown--label").all_inner_texts()

    def repository_name_locator(self) -> Locator:
        return self.page.get_by_label("Repository name")

    def default_branch_name_locator(self) -> Locator:
        return self.page.locator("#id_branch_name")

    def create_repository_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Create repository")

    def cancel_creation_button_locator(self) -> Locator:
        return self.page.get_by_role("link", name="Cancel")


class CreateRepositoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.url = "https://bitbucket.org/auto-bucket-pl2/workspace/create/repository"
        self.locators = CreateRepositoryLocators(self.page)

    def is_create_new_repository_visible(self) -> bool:
        return True if self.locators.heading_page_locator().is_visible() else False

    def select_project(self, proj_name: str) -> None:
        proj_name = proj_name
        self.locators.select_project_dropdown_locator().click()
        page_log.debug(f"Found project: {proj_name}")
        self.locators.select_project_locator(proj_name).click()

    def fill_in_project_name_input(self, project_name: str) -> None:
        self.locators.project_name_input_locator().click()
        self.locators.project_name_input_locator().fill(project_name)

    def fill_in_repository_name_input(self, repository_name: str) -> None:
        self.locators.repository_name_locator().click()
        self.locators.repository_name_locator().fill(repository_name)

    def fill_in_default_branch_name_input(self, branch_name: str = "master") -> None:
        self.locators.default_branch_name_locator().click()
        self.locators.default_branch_name_locator().fill(branch_name)

    def click_on_create_repository_button(self) -> None:
        self.locators.create_repository_button_locator().click()

    def click_on_cancel_button(self) -> None:
        self.locators.cancel_creation_button_locator().click()

    def fill_in_repository_creation_form(self, new_repo_data: dict) -> None:
        time.sleep(3)
        page_log.info("Selecting Project")
        self.select_project(new_repo_data["project_name"])
        page_log.info("Filling in repository name")
        self.fill_in_repository_name_input(new_repo_data["repository_name"])
        page_log.info("Filling in branch name")
        self.fill_in_default_branch_name_input(new_repo_data["branch_name"])
        page_log.info("Saving and continue")
        self.click_on_create_repository_button()
