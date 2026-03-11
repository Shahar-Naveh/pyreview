"""Rich terminal display for review results."""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from pyreview.core.schemas import ReviewResult, Severity

SEVERITY_COLORS = {
    Severity.CRITICAL: "bold red",
    Severity.HIGH: "red",
    Severity.MEDIUM: "yellow",
    Severity.LOW: "cyan",
    Severity.INFO: "dim",
}


def display_review_result(result: ReviewResult, console: Console) -> None:
    """Render the full review result to the terminal."""

    # --- Summary Panel ---
    if result.summary:
        s = result.summary
        score_color = (
            "green" if s.overall_score >= 7
            else "yellow" if s.overall_score >= 4
            else "red"
        )
        summary_text = Text()
        summary_text.append(
            f"Score: {s.overall_score}/10", style=f"bold {score_color}"
        )
        summary_text.append(f"  |  Verdict: {s.verdict.upper()}\n\n")
        summary_text.append(s.executive_summary)

        if s.strengths:
            summary_text.append("\n\nStrengths:\n", style="bold green")
            for strength in s.strengths:
                summary_text.append(f"  + {strength}\n")

        if s.top_concerns:
            summary_text.append("\nConcerns:\n", style="bold red")
            for concern in s.top_concerns:
                summary_text.append(f"  - {concern}\n")

        console.print(
            Panel(summary_text, title="Review Summary", border_style="blue")
        )

    # --- Findings Table ---
    table = Table(
        title=f"Findings ({len(result.all_findings)})", show_lines=True
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Sev", width=10)
    table.add_column("Agent", width=14)
    table.add_column("Title", min_width=30)
    table.add_column("File", min_width=20)
    table.add_column("Line", width=6)

    for i, f in enumerate(result.all_findings, 1):
        sev_style = SEVERITY_COLORS.get(f.severity, "")
        table.add_row(
            str(i),
            Text(f.severity.value.upper(), style=sev_style),
            f.agent,
            f.title,
            f.location.file,
            str(f.location.start_line),
        )

    console.print(table)

    # --- Detailed Findings with Fix Suggestions ---
    for f in result.all_findings:
        if f.fix_suggestion:
            sev_style = SEVERITY_COLORS.get(f.severity, "")
            panel_content = Text()
            panel_content.append(f"{f.description}\n\n", style="dim")
            panel_content.append("Suggested fix:\n", style="bold")

            console.print(
                Panel(
                    panel_content,
                    title=f"[{f.severity.value.upper()}] {f.title}",
                    border_style=sev_style.replace("bold ", ""),
                )
            )
            if f.fix_suggestion.diff:
                console.print(Syntax(
                    f.fix_suggestion.diff,
                    "diff",
                    theme="monokai",
                    line_numbers=False,
                ))
            console.print()

    # --- Stats ---
    console.print(
        f"\n[dim]Time: {result.total_execution_time_seconds}s | "
        f"Tokens: {result.total_token_usage}[/dim]"
    )
