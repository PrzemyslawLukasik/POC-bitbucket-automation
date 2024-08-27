import json
from pathlib import Path

from requests.auth import HTTPBasicAuth
from requests.models import Response
from slugify import slugify

from src.helpers.api_client import APIClient


class BitBucketClient(APIClient):
    def __init__(self, base_url: str, auth: HTTPBasicAuth):
        base_url = base_url
        super().__init__(base_url=base_url, auth=auth)

    def add_repository(self, repo_data: dict) -> Response:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        payload = json.dumps(repo_data)
        slug = slugify(str(repo_data["full_name"]))
        response = self.post(f"/{slug}", data=payload, headers=headers)
        return response

    def get_repositories(self) -> Response:
        headers = {"Accept": "application/json"}
        response = self.get("/", headers=headers)
        return response

    def remove_repository(self, repo_slug: str) -> Response:
        headers = {"Aaccept": "application/json"}
        response = self.delete(f"/{repo_slug}", headers=headers)
        return response

    def upload_file(self, repo_slug: str, name: str, path: Path) -> Response:
        files = {name: open(f"{path}", "rb")}
        response = self.post(f"/{repo_slug}/src", files=files)
        return response

    def get_list_of_commits(self, repo_slug: str) -> Response:
        headers = {"Accept": "application/json"}
        response = self.get(f"/{repo_slug}/commits", headers=headers)
        return response

    def get_a_commit(self, repo_slug: str, commit: str) -> Response:
        headers = {"Accept": "application/json"}
        response = self.get(f"/{repo_slug}/commit/{commit}", headers=headers)
        return response

    def remove_list_of_repositories(self, slugs: list) -> None:
        for item in slugs:
            self.remove_repository(item)
