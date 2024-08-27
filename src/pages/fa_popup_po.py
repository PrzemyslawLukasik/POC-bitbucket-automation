from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass
class FaPopupLocators:
    def __init__(self, page: Page):
        self.page = page

    def fa_heading_locator(self) -> Locator:
        return self.page.get_by_role("heading", name="Enable two-step verification")

    def fa_continue_without_button_locator(self) -> Locator:
        return self.page.get_by_role("button", name="Continue without two-step")

    def dashboard_link_locator(self) -> Locator:
        self.page.get_by_role("link", name="dashboard")


class FaPopupPo:
    def __init__(self, page: Page):
        self.page = page
        self.locators = FaPopupLocators(self.page)

    def fa_header_visible(self) -> bool:
        return (
            True
            if self.locators.fa_heading_locator().is_visible(timeout=10000)
            else False
        )

    def click_on_continue_without_link(self) -> None:
        self.locators.fa_continue_without_button_locator().click()

    def is_dashboard_link_visible(self) -> bool:
        self.page.wait_for_load_state("load", timeout=10000)
        return (
            True
            if self.locators.dashboard_link_locator().is_visible(timeout=10000)
            else False
        )

    def click_on_dashboard_link(self) -> None:
        self.locators.dashboard_link_locator().click()
