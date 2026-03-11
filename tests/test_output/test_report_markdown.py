"""Tests for Markdown report generation."""

from pyreview.core.schemas import (
    Category,
    CodeLocation,
    Finding,
    FileToReview,
    FixSuggestion,
    ReviewRequest,
    ReviewResult,
    ReviewStatus,
    ReviewSummary,
    Severity,
)
from pyreview.output.report_markdown import generate_markdown_report


def test_markdown_report_contains_summary():
    request = ReviewRequest(
        files=[FileToReview(path="test.py", content="x = 1")],
    )
    result = ReviewResult(
        request=request,
        status=ReviewStatus.COMPLETED,
        summary=ReviewSummary(
            overall_score=6.5,
            verdict="comment",
            executive_summary="Some issues found.",
            strengths=["Good naming"],
            top_concerns=["Missing validation"],
        ),
    )

    md = generate_markdown_report(result)

    assert "# Code Review Report" in md
    assert "6.5/10" in md
    assert "comment" in md
    assert "Good naming" in md
    assert "Missing validation" in md


def test_markdown_report_contains_findings():
    request = ReviewRequest(
        files=[FileToReview(path="test.py", content="x = 1")],
    )
    result = ReviewResult(
        request=request,
        status=ReviewStatus.COMPLETED,
        all_findings=[
            Finding(
                agent="style",
                category=Category.STYLE,
                severity=Severity.LOW,
                title="Missing docstring",
                description="Function lacks docstring",
                location=CodeLocation(file="test.py", start_line=5),
                fix_suggestion=FixSuggestion(
                    description="Add docstring",
                    original_code="def foo():",
                    suggested_code='def foo():\n    """Do foo."""',
                    diff="- def foo():\n+ def foo():\n+     \"\"\"Do foo.\"\"\"",
                ),
            )
        ],
    )

    md = generate_markdown_report(result)

    assert "Missing docstring" in md
    assert "test.py" in md
    assert "Suggested fix:" in md
