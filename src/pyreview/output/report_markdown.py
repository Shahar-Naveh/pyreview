"""Generate a human-readable Markdown report from ReviewResult."""

from pyreview.core.schemas import ReviewResult, Severity


SEVERITY_MARKER = {
    Severity.CRITICAL: "!!",
    Severity.HIGH: "!",
    Severity.MEDIUM: "~",
    Severity.LOW: "-",
    Severity.INFO: "i",
}


def generate_markdown_report(result: ReviewResult) -> str:
    lines = []
    summary = result.summary

    lines.append("# Code Review Report\n")

    if summary:
        lines.append(
            f"**Score: {summary.overall_score}/10** | "
            f"**Verdict: {summary.verdict}**\n"
        )
        lines.append(f"{summary.executive_summary}\n")

        if summary.strengths:
            lines.append("## Strengths")
            for s in summary.strengths:
                lines.append(f"- {s}")
            lines.append("")

        if summary.top_concerns:
            lines.append("## Top Concerns")
            for c in summary.top_concerns:
                lines.append(f"- {c}")
            lines.append("")

    lines.append("## Findings\n")

    by_severity: dict[Severity, list] = {}
    for f in result.all_findings:
        by_severity.setdefault(f.severity, []).append(f)

    for sev in Severity:
        findings = by_severity.get(sev, [])
        if not findings:
            continue
        lines.append(f"### {sev.value.upper()} ({len(findings)})\n")
        for f in findings:
            marker = SEVERITY_MARKER[sev]
            lines.append(f"#### [{marker}] {f.title}")
            lines.append(
                f"**Agent**: {f.agent} | **File**: `{f.location.file}` "
                f"L{f.location.start_line}"
            )
            lines.append(f"\n{f.description}\n")
            if f.fix_suggestion:
                lines.append("**Suggested fix:**")
                lines.append(f"```diff\n{f.fix_suggestion.diff}\n```\n")

    lines.append(
        f"---\n*Generated in {result.total_execution_time_seconds}s | "
        f"Tokens: {result.total_token_usage}*\n"
    )

    return "\n".join(lines)
