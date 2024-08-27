import logging

from playwright.sync_api import Page

page_log = logging.getLogger("PAGE")


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""

    def visit(self) -> None:
        page_log.info(f"Visiting page: {self.url}")
        self.page.goto(self.url)
