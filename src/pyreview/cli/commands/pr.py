"""pyreview pr <url> -- review a GitHub pull request."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from pyreview.agents.orchestrator import Orchestrator
from pyreview.cli.display import display_review_result
from pyreview.core.config import Settings
from pyreview.ingest.github_client import GitHubClient
from pyreview.output.diff_generator import enrich_findings_with_diffs
from pyreview.output.github_publisher import GitHubPublisher
from pyreview.output.report_json import generate_json_report
from pyreview.output.report_markdown import generate_markdown_report

console = Console()


def pr_command(
    pr_url: str = typer.Argument(..., help="GitHub PR URL"),
    config: Path = typer.Option(
        Path("config.yaml"), help="Config file path"
    ),
    publish: bool = typer.Option(
        False, help="Post review comments to GitHub"
    ),
    output_json: Optional[Path] = typer.Option(None, "--json"),
    output_md: Optional[Path] = typer.Option(None, "--md"),
) -> None:
    """Review a GitHub pull request."""
    settings = Settings.from_yaml(config)

    gh_client = GitHubClient(settings)
    console.print(f"[bold]Fetching PR: {pr_url}...[/bold]")
    request = gh_client.fetch_pr(pr_url)

    console.print(
        f"[bold]Found {len(request.files)} Python file(s). Reviewing...[/bold]\n"
    )

    orchestrator = Orchestrator(settings)
    result = asyncio.run(
        orchestrator.run(request, progress_callback=_cli_progress)
    )
    result.all_findings = enrich_findings_with_diffs(result.all_findings)

    display_review_result(result, console)

    if output_json:
        generate_json_report(result, output_json)
        console.print(f"[green]JSON report written to {output_json}[/green]")
    if output_md:
        md = generate_markdown_report(result)
        output_md.write_text(md, encoding="utf-8")
        console.print(f"[green]Markdown report written to {output_md}[/green]")

    if publish:
        publisher = GitHubPublisher(settings)
        review_url = publisher.publish_review(result)
        console.print(
            f"\n[bold green]Review published: {review_url}[/bold green]"
        )


def _cli_progress(agent_name: str, status: str) -> None:
    if status == "started":
        console.print(
            f"  [dim]Agent [bold]{agent_name}[/bold] started...[/dim]"
        )
    elif status == "completed":
        console.print(
            f"  [green]Agent [bold]{agent_name}[/bold] completed.[/green]"
        )
