"""Generate unified diffs for fix suggestions."""

import difflib

from pyreview.core.schemas import Finding


def generate_fix_diff(finding: Finding) -> str | None:
    """Produce a unified diff string from a finding's fix suggestion."""
    if not finding.fix_suggestion:
        return None

    fix = finding.fix_suggestion
    original_lines = fix.original_code.splitlines(keepends=True)
    suggested_lines = fix.suggested_code.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        suggested_lines,
        fromfile=f"a/{finding.location.file}",
        tofile=f"b/{finding.location.file}",
        lineterm="",
    )
    return "\n".join(diff)


def enrich_findings_with_diffs(findings: list[Finding]) -> list[Finding]:
    """Post-process findings to fill in the diff field on fix suggestions."""
    for f in findings:
        if f.fix_suggestion and not f.fix_suggestion.diff:
            diff_text = generate_fix_diff(f)
            if diff_text:
                f.fix_suggestion.diff = diff_text
    return findings
