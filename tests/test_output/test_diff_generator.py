"""Tests for diff generator."""

from pyreview.core.schemas import (
    Category,
    CodeLocation,
    Finding,
    FixSuggestion,
    Severity,
)
from pyreview.output.diff_generator import enrich_findings_with_diffs, generate_fix_diff


def test_generate_fix_diff():
    finding = Finding(
        agent="security",
        category=Category.SECURITY,
        severity=Severity.HIGH,
        title="Command Injection",
        description="desc",
        location=CodeLocation(file="app.py", start_line=5),
        fix_suggestion=FixSuggestion(
            description="Use subprocess",
            original_code="os.system(cmd)",
            suggested_code="subprocess.run(cmd, shell=False)",
        ),
    )

    diff = generate_fix_diff(finding)
    assert diff is not None
    assert "os.system(cmd)" in diff
    assert "subprocess.run(cmd, shell=False)" in diff


def test_generate_fix_diff_returns_none_without_suggestion():
    finding = Finding(
        agent="style",
        category=Category.STYLE,
        severity=Severity.LOW,
        title="Naming",
        description="desc",
        location=CodeLocation(file="app.py", start_line=1),
    )

    assert generate_fix_diff(finding) is None


def test_enrich_findings_fills_diff():
    findings = [
        Finding(
            agent="perf",
            category=Category.PERFORMANCE,
            severity=Severity.MEDIUM,
            title="Slow loop",
            description="desc",
            location=CodeLocation(file="calc.py", start_line=10),
            fix_suggestion=FixSuggestion(
                description="Use numpy",
                original_code="for x in arr: total += x",
                suggested_code="total = np.sum(arr)",
            ),
        )
    ]

    enriched = enrich_findings_with_diffs(findings)
    assert enriched[0].fix_suggestion.diff != ""
