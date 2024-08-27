import logging
import os
import time
from pathlib import Path

import pytest
from playwright.sync_api import Page
from requests import Response

from src.fixtures.api_fixtures import (
    api_client,
    create_and_delete_repository,
    create_repository,
    get_repositories,
)
from src.helpers.bitbucket_api import BitBucketClient
from src.helpers.generators import generate_new_repo_data_api, generate_new_repo_data_ui
from src.helpers.git_helper import clone_repository, create_repo_folder, remove_repo
from src.helpers.requests_filtering import verify_repository_name_in_response
from src.pages.dashboard.dashboard_page import DashboardPage
from src.pages.login_page import LoginPage
from src.pages.repository.repositories_list_page import RepositoriesListPage
from src.pages.repository.repository_create_form_page import CreateRepositoryPage
from src.pages.repository.repository_page.repository_page import RepositoryPage
from src.pages.repository.repository_page.source_po import RepositorySourcePo
from src.pages.top_bar import TopBarPo

test_log = logging.getLogger("TEST")


@pytest.mark.UI
def test_repository_creation(api_client: Response, admin_page: Page) -> None:
    # Pre-condition
    top_bar = TopBarPo(admin_page)
    login_page = LoginPage(admin_page)
    dashboard = DashboardPage(admin_page)
    create_repo = CreateRepositoryPage(admin_page)
    repository_list = RepositoriesListPage(admin_page)
    login_page.visit()

    # Repository creation
    dashboard.top_bar.click_on_create_button()
    dashboard.top_bar.click_on_repository_create_item()
    new_repository_data = next(generate_new_repo_data_ui())
    create_repo.fill_in_repository_creation_form(new_repository_data)

    # Verification
    top_bar.click_on_repositories_item()
    assert repository_list.search_for_repository(
        new_repository_data["repository_name"]
    ), f"No {new_repository_data['repository_name']} found."

    # Clean up
    api_client.remove_repository(new_repository_data["repository_name"])


@pytest.mark.API
def test_create_a_repo(
    create_and_delete_repository: Response, get_repositories: Response
) -> None:
    # Create a repository
    repo = create_and_delete_repository

    # Get a list of repositories
    list_of_repositories = get_repositories

    # Verify created repository name in list of repositories
    assert verify_repository_name_in_response(
        list_of_repositories, repo.json()["name"]
    ), "Repository not created"


@pytest.mark.UI
# @pytest.mark.dev
def test_change_code_via_ui(
    create_and_delete_repository: Response, admin_page: Page
) -> None:
    # Pre-condition
    repository_list_page = RepositoriesListPage(admin_page)
    repository_page = RepositoryPage(admin_page)
    # Create a repository
    repository = create_and_delete_repository

    # Go to repository page
    repository_list_page.visit()
    repository_list_page.search_for_repository(repository.json()["name"])
    repository_list_page.select_repository(repository.json()["name"])

    # Add a README.md file
    repository_page.create_default_readme_file()
    # Edit README.md file and save
    repository_page.edit_readme_file_content("EDITED\n")
    # Verify changes are saved
    repository_page.source_view.verify_that_readme_include("EDITED")


@pytest.mark.UI
def test_submit_code_changes_via_ui(
    create_and_delete_repository: Response, admin_page: Page
) -> None:
    # Pre-condition
    repository_list_page = RepositoriesListPage(admin_page)
    repository_page = RepositoryPage(admin_page)
    # Create a repository
    repository = create_and_delete_repository

    # Go to created repository
    repository_list_page.visit()
    repository_list_page.search_for_repository(repository.json()["name"])
    repository_list_page.select_repository(repository.json()["name"])
    # Add README.md and save it
    repository_page.create_default_readme_file()
    # Go to branches
    repository_page.sidebar.click_on_branches_link()
    # Create a new branch
    repository_page.branches_view.create_new_branch("test_branch")
    repository_page.sidebar.click_on_source_link()
    repository_page.source_view.change_branch_to("test_branch")
    # Edit readme file and commit changes
    repository_page.edit_readme_file_content("EDITED WITH MR\n")
    # Compare to master and create a PR
    repository_page.source_view.change_branch_to("test_branch")
    repository_page.source_view.compare_branches()
    repository_page.branches_view.locators.compare_button_locator().wait_for(
        state="visible"
    )
    repository_page.sidebar.locators.source_link_locator().wait_for(state="visible")
    repository_page.branches_view.click_on_compare_button()
    repository_page.branches_view.click_on_merge_button()
    # Merge PR and review changes on README.md on master branch.
    repository_page.branches_view.merge_changes_to_master("test_branch")
    repository_page.sidebar.click_on_source_link()
    repository_page.source_view.verify_that_readme_include("EDITED")


@pytest.mark.API
def test_clone_repository(api_client, create_and_delete_repository: Response):
    repo = create_and_delete_repository
    origin_url = repo.json()["links"]["clone"][0]["href"]

    # Upload file through BitBucket API
    repo_api: BitBucketClient = api_client
    repo_api.upload_file(
        repo.json()["name"], name="README.md", path=Path("src/payloads/README.md")
    )

    # Clone the repo to a temp folder
    repo_folder_path = create_repo_folder(repo.json()["name"])
    clone_repository(origin_url, repo_folder_path)

    # Verify the uploaded file exist in clonned repository
    assert "README.md" in os.listdir(repo_folder_path), "Repository not  cloned"
    remove_repo(repo_folder_path)


@pytest.mark.API
def test_file_upload_via_api(api_client, create_and_delete_repository: Response):
    repo = create_and_delete_repository
    # Upload file through BitBucket API
    repo_api: BitBucketClient = api_client
    pre_upload_list = repo_api.get_list_of_commits(repo.json()["name"])
    repo_api.upload_file(
        repo.json()["name"], name="README.md", path=Path("src/payloads/README.md")
    )
    # verify last commit reflects the upload.
    after_upload_list = repo_api.get_list_of_commits(repo.json()["name"])

    assert after_upload_list.json()["values"] is not pre_upload_list.json()["values"]
