import os
import shutil
from pathlib import Path

from git import Repo


def create_repo_folder(folder_name: str) -> Path:
    base_dir = os.path.abspath("/tmp/")
    repo_dir = os.path.join(os.path.abspath(base_dir), folder_name)
    return Path(repo_dir)


def clone_repository(remote_path, local_path: Path) -> Repo:
    repo = Repo.clone_from(remote_path, local_path)
    return repo


def get_latest_commit(repo: Repo):
    return repo.head.commit.tree


def remove_repo(repo_dir: str) -> None:
    shutil.rmtree(repo_dir)
