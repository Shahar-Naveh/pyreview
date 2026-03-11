"""Typer application root."""

import typer

from pyreview.cli.commands import config_cmd, pr, review, server

app = typer.Typer(
    name="pyreview",
    help="AI-powered multi-agent Python code review",
    no_args_is_help=True,
)

app.command(name="review")(review.review_command)
app.command(name="pr")(pr.pr_command)
app.command(name="serve")(server.serve_command)
app.command(name="config")(config_cmd.config_command)

if __name__ == "__main__":
    app()
