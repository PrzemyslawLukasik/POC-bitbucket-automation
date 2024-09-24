import logging
import os
from typing import Generator

import pytest
from requests.auth import HTTPBasicAuth
from requests.models import Response
from slugify import slugify

from src.helpers.bitbucket_api import BitBucketClient
from src.helpers.generators import generate_new_repo_data_api

fix_log = logging.getLogger("FIXTURE")


@pytest.fixture(scope="session", autouse=True)
def api_client() -> BitBucketClient:
    auth = HTTPBasicAuth(os.environ["API_USER"], os.environ["API_PASS"])
    base_url = os.environ["API_URL"]
    fix_log.debug(f"base_url: {base_url}")
    fix_log.debug(f"auth: {auth}")
    return BitBucketClient(base_url=base_url, auth=auth)


@pytest.fixture(scope="function")
def create_repository(api_client) -> Generator[Response, None, None]:
    repository_data = next(generate_new_repo_data_api())
    fix_log.debug(f"Repository data: {repository_data}")
    repo = api_client.add_repository(repository_data)
    fix_log.debug(f"New repository created:\n{repo}")
    yield repo


@pytest.fixture(scope="function")
def get_repositories(api_client) -> Generator[Response, None, None]:
    repo_list = api_client.get_repositories()
    yield repo_list


@pytest.fixture(scope="function")
def create_and_delete_repository(
    api_client, create_repository
) -> Generator[Response, None, None]:
    repo = create_repository
    yield repo
    api_client.remove_repository(slugify(repo.json()["name"]))
