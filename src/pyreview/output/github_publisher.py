"""Post review findings as GitHub PR review comments."""

from __future__ import annotations

from github import Auth, Github

from pyreview.core.config import Settings
from pyreview.core.schemas import Finding, ReviewResult


class GitHubPublisher:
    def __init__(self, settings: Settings):
        token = settings.github_token
        if token is None:
            raise ValueError("GitHub token required to publish review")
        self.gh = Github(auth=Auth.Token(token.get_secret_value()))

    def publish_review(self, result: ReviewResult) -> str:
        """
        Post a PR review with inline comments for each finding.
        Returns the URL of the created review.
        """
        if not result.request.repo_full_name or not result.request.pr_number:
            raise ValueError("ReviewResult must have repo and PR info")

        repo = self.gh.get_repo(result.request.repo_full_name)
        pr = repo.get_pull(result.request.pr_number)
        commit = repo.get_commit(pr.head.sha)

        comments = []
        for finding in result.all_findings:
            body = self._format_comment(finding)
            comments.append({
                "path": finding.location.file,
                "line": finding.location.start_line,
                "body": body,
            })

        event = "COMMENT"
        if result.summary and result.summary.verdict == "request_changes":
            event = "REQUEST_CHANGES"
        elif result.summary and result.summary.verdict == "approve":
            event = "APPROVE"

        body = ""
        if result.summary:
            body = (
                f"## pyreview - Automated Code Review\n\n"
                f"**Score: {result.summary.overall_score}/10**\n\n"
                f"{result.summary.executive_summary}"
            )

        review = pr.create_review(
            commit=commit,
            body=body,
            event=event,
            comments=comments,
        )
        return review.html_url

    @staticmethod
    def _format_comment(finding: Finding) -> str:
        """Format a single finding as a GitHub review comment."""
        parts = [
            f"**[{finding.severity.value.upper()}]** {finding.title}",
            f"*Agent: {finding.agent} | Confidence: {finding.confidence:.0%}*",
            "",
            finding.description,
        ]
        if finding.fix_suggestion:
            parts.append("")
            parts.append("**Suggested fix:**")
            parts.append(
                f"```suggestion\n{finding.fix_suggestion.suggested_code}\n```"
            )
        if finding.references:
            parts.append("")
            parts.append("**References:** " + ", ".join(finding.references))
        return "\n".join(parts)
