"""pyreview review <paths...> -- review local files."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from pyreview.agents.orchestrator import Orchestrator
from pyreview.cli.display import display_review_result
from pyreview.core.config import Settings
from pyreview.core.schemas import ReviewRequest
from pyreview.ingest.file_loader import load_files
from pyreview.output.diff_generator import enrich_findings_with_diffs
from pyreview.output.report_json import generate_json_report
from pyreview.output.report_markdown import generate_markdown_report

console = Console()


def review_command(
    paths: list[Path] = typer.Argument(..., help="Files or directories to review"),
    config: Path = typer.Option(
        Path("config.yaml"), help="Config file path"
    ),
    output_json: Optional[Path] = typer.Option(
        None, "--json", help="Write JSON report"
    ),
    output_md: Optional[Path] = typer.Option(
        None, "--md", help="Write Markdown report"
    ),
    severity: Optional[str] = typer.Option(
        None, help="Minimum severity filter"
    ),
    agents: Optional[str] = typer.Option(
        None, help="Comma-separated agent names to run"
    ),
    no_parallel: bool = typer.Option(
        False, help="Run agents sequentially"
    ),
) -> None:
    """Review Python files using AI agents."""
    settings = Settings.from_yaml(config)
    if no_parallel:
        settings.parallel_agents = False
    if severity:
        settings.severity_threshold = severity

    if agents:
        enabled = set(agents.split(","))
        for name in ("security", "performance", "style", "architecture", "engineering"):
            cfg = getattr(settings, name)
            cfg.enabled = name in enabled

    files = load_files(paths, settings)
    if not files:
        console.print("[red]No Python files found.[/red]")
        raise typer.Exit(1)

    console.print(f"[bold]Reviewing {len(files)} file(s)...[/bold]\n")
    request = ReviewRequest(files=files, source="cli")

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


def _cli_progress(agent_name: str, status: str) -> None:
    if status == "started":
        console.print(
            f"  [dim]Agent [bold]{agent_name}[/bold] started...[/dim]"
        )
    elif status == "completed":
        console.print(
            f"  [green]Agent [bold]{agent_name}[/bold] completed.[/green]"
        )
