"""pyreview config -- show/validate configuration."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from pyreview.core.config import Settings

console = Console()


def config_command(
    config: Path = typer.Option(
        Path("config.yaml"), help="Config file path"
    ),
) -> None:
    """Show current pyreview configuration."""
    try:
        settings = Settings.from_yaml(config)
    except Exception as e:
        console.print(f"[red]Config error: {e}[/red]")
        raise typer.Exit(1)

    table = Table(title="PyReview Configuration")
    table.add_column("Setting", style="bold")
    table.add_column("Value")

    # API keys (masked)
    api_key = settings.anthropic_api_key.get_secret_value()
    masked_key = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "(not set)"
    table.add_row("Anthropic API Key", masked_key)

    gh_token = settings.github_token
    if gh_token:
        t = gh_token.get_secret_value()
        masked_t = f"{t[:6]}...{t[-4:]}" if len(t) > 10 else "(set)"
        table.add_row("GitHub Token", masked_t)
    else:
        table.add_row("GitHub Token", "(not set)")

    table.add_row("Default Model", settings.default_model)
    table.add_row("Orchestrator Model", settings.orchestrator_model)
    table.add_row("Parallel Agents", str(settings.parallel_agents))
    table.add_row("Severity Threshold", settings.severity_threshold)
    table.add_row("Max Files", str(settings.max_files))
    table.add_row("Max File Size (KB)", str(settings.max_file_size_kb))
    table.add_row("Web Host", f"{settings.web_host}:{settings.web_port}")
    table.add_row("DB Path", settings.db_path)

    console.print(table)

    # Agent status
    agent_table = Table(title="Agents")
    agent_table.add_column("Agent", style="bold")
    agent_table.add_column("Enabled")
    agent_table.add_column("Model")
    agent_table.add_column("Temperature")

    for name in ("security", "performance", "style", "architecture", "engineering"):
        cfg = getattr(settings, name)
        status = "[green]ON[/green]" if cfg.enabled else "[red]OFF[/red]"
        agent_table.add_row(name, status, cfg.model, str(cfg.temperature))

    console.print(agent_table)
