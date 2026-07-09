import os
import shutil

from git import Repo
from git.exc import GitCommandError


class GitHubLoader:

    def __init__(self, base_path="data/repos"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def clone_repo(self, repo_url: str) -> str:

        if not repo_url.startswith("https://github.com/"):
            raise ValueError("Please enter a valid GitHub repository URL.")

        repo_name = repo_url.rstrip("/").split("/")[-1]

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        repo_path = os.path.join(self.base_path, repo_name)

        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        try:
            Repo.clone_from(repo_url, repo_path)

        except GitCommandError:
            raise ValueError(
                "Unable to clone repository. Please ensure the repository exists and is public."
            )

        return repo_path