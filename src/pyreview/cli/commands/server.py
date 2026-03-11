"""pyreview serve -- start the web dashboard."""

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def serve_command(
    config: Path = typer.Option(
        Path("config.yaml"), help="Config file path"
    ),
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload for development"),
) -> None:
    """Start the pyreview web dashboard."""
    import uvicorn

    from pyreview.core.config import Settings

    settings = Settings.from_yaml(config)
    settings.web_host = host
    settings.web_port = port

    console.print(
        f"[bold green]Starting pyreview dashboard at "
        f"http://{host}:{port}[/bold green]"
    )

    uvicorn.run(
        "pyreview.web.app:create_app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
    )
