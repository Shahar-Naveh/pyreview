"""Fetch PR diffs and file contents via PyGithub."""

from __future__ import annotations

import re

from github import Auth, Github

from pyreview.core.config import Settings
from pyreview.core.schemas import FileToReview, ReviewRequest


class GitHubClient:
    def __init__(self, settings: Settings):
        token = settings.github_token
        if token is None:
            raise ValueError("PYREVIEW_GITHUB_TOKEN is required for PR reviews")
        auth = Auth.Token(token.get_secret_value())
        self.gh = Github(auth=auth)

    def fetch_pr(self, pr_url: str) -> ReviewRequest:
        """
        Parse a PR URL like https://github.com/owner/repo/pull/42
        and return a ReviewRequest with file contents and diffs.
        """
        owner, repo, pr_number = self._parse_pr_url(pr_url)
        repo_obj = self.gh.get_repo(f"{owner}/{repo}")
        pr = repo_obj.get_pull(pr_number)

        files: list[FileToReview] = []
        for pr_file in pr.get_files():
            if not pr_file.filename.endswith(".py"):
                continue
            if pr_file.status == "removed":
                continue

            try:
                content_file = repo_obj.get_contents(
                    pr_file.filename, ref=pr.head.sha
                )
                content = content_file.decoded_content.decode("utf-8")
            except Exception:
                content = ""

            files.append(FileToReview(
                path=pr_file.filename,
                content=content,
                language="python",
                diff=pr_file.patch,
            ))

        return ReviewRequest(
            files=files,
            source="pr",
            pr_url=pr_url,
            pr_number=pr_number,
            repo_full_name=f"{owner}/{repo}",
        )

    @staticmethod
    def _parse_pr_url(url: str) -> tuple[str, str, int]:
        match = re.match(
            r"https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)", url
        )
        if not match:
            raise ValueError(f"Invalid GitHub PR URL: {url}")
        return match.group(1), match.group(2), int(match.group(3))
