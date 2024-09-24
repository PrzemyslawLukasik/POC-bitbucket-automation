"""This conftest.py module is automatically loaded during framework execution
    It includes mostly pytest framework configuration.
"""

import os
import time
from datetime import datetime
from pathlib import Path

import dotenv
import pytest
import pytest_playwright
from playwright.sync_api import Browser, Page, Playwright

from src.helpers.screenshots import Screenshots
from src.pages.login_page import LoginPage
from src.pages.top_bar import TopBarPo

dotenv.load_dotenv()


LOGGERS = "TEST,PAGE,FIXTURE,API,GENERATOR"
LOG_LEVEL = "debug"


def pytest_logger_config(logger_config):
    logger_config.add_loggers(
        ["TEST", "PAGE", "FIXTURE", "API", "GENERATOR"], stdout_level=LOG_LEVEL
    )
    logger_config.set_log_option_default(LOGGERS)


def pytest_logger_logdirlink(config):
    return os.path.join(os.path.dirname(__file__), "logs")


@pytest.fixture
def page(page: Page) -> Page:
    return page


def pytest_addoption(parser):
    parser.addoption(
        "--screenshot-path",
        action="store",
        dest="screenshot_path",
        default="artefacts/screenshots",
        help="Path to the screenshots folder",
    )
    parser.addoption(
        "--additional-info",
        action="store",
        dest="additional_info",
        default="Build: ",
        help="Path to the screenshots folder",
    )
    parser.addoption(
        "--tracing-path",
        action="store",
        dest="tracing_path",
        default="artefacts/tracing",
        help="Path to store tracing",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screenshot_path = ""
    report = outcome.get_result()

    setattr(item, "rep_" + report.when, report)
    extras = getattr(report, "extras", [])
    if report.when == "call" and "page" in item.funcargs:
        if report.failed and "page" in item.funcargs:
            page = item.funcargs["page"]
            tracing_path = item.config.option.tracing_path + "/" + item.name + ".zip"
            page.context.tracing.stop(path=tracing_path)
            screenshot_path = item.config.option.screenshot_path
            if screenshot_path:
                screenshots = Screenshots(
                    relative_path=Path(screenshot_path), page=page
                )
                screenshots.save_screenshot_as_file(item.name)
            screenshot_base64 = Screenshots(
                relative_path=Path(""), page=page
            ).save_screenshot_as_base64()
            extras.append(pytest_html.extras.image(screenshot_base64))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # add the screenshots to the html report
            page = item.funcargs["page"]
            screenshot_base64 = Screenshots(
                relative_path=Path(""), page=page
            ).save_screenshot_as_base64()
            extras.append(pytest_html.extras.image(screenshot_base64))
        report.extras = extras


def pytest_html_report_title(report):
    date = datetime.now().strftime("%B %d %Y %H:%M:%S")
    report.title = f"Report for automation run on {date}"
