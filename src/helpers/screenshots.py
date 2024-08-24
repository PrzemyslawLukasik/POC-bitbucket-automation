import base64
from pathlib import Path

from playwright.sync_api import Page


class Screenshots:
    """
    A class to prepare a screenshot and a place for it

    Args:
        relative_path (Path): a relative path to thhe screenshots folder
        page (Page): a page object (driver)

    """

    def __init__(self, relative_path: Path, page: Page):
        self.page = page
        self.screenshots_path = Path.cwd() / relative_path

    def delete_all_screenshots(self):
        """
        Deletes all data from path provided in __init__
        """
        if self.screenshots_path.exists():
            [f.unlink() for f in self.screenshots_path.glob("*") if f.is_file()]

    def save_screenshots_as_dir(self):
        """
        Saves screenshots dir if it doesn't exists
        """
        if not self.screenshots_path.exists():
            Path.mkdir(self.screenshots_path, parents=True)
        return self.screenshots_path

    def save_screenshot_as_file(self, name: str) -> Path:
        """
        Takes screenshot and saves it as file with provided name
        """
        screenshots_path = self.save_screenshots_as_dir()
        screenshot_file_path = Path(screenshots_path / f"{name}.png")
        self.page.screenshot(path=str(screenshot_file_path))
        return screenshot_file_path

    def save_screenshot_as_base64(self):
        """
        Gets screenshot of the page as a base64
        """
        screenshot_bytes = self.page.screenshot()
        return base64.b64encode(screenshot_bytes).decode()
