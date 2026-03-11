"""Tests for JSON report generation."""

import json

from pyreview.core.schemas import (
    Category,
    CodeLocation,
    Finding,
    FileToReview,
    ReviewRequest,
    ReviewResult,
    ReviewStatus,
    ReviewSummary,
    Severity,
)
from pyreview.output.report_json import generate_json_report


def test_generate_json_report():
    request = ReviewRequest(
        files=[FileToReview(path="test.py", content="x = 1")],
        source="cli",
    )
    result = ReviewResult(
        request=request,
        status=ReviewStatus.COMPLETED,
        all_findings=[
            Finding(
                agent="security",
                category=Category.SECURITY,
                severity=Severity.HIGH,
                title="Test Finding",
                description="Test description",
                location=CodeLocation(file="test.py", start_line=1),
            )
        ],
        summary=ReviewSummary(
            overall_score=7.0,
            verdict="approve",
            executive_summary="Looks good.",
        ),
    )

    json_str = generate_json_report(result)
    parsed = json.loads(json_str)

    assert parsed["status"] == "completed"
    assert len(parsed["all_findings"]) == 1
    assert parsed["summary"]["overall_score"] == 7.0


def test_generate_json_report_to_file(tmp_path):
    request = ReviewRequest(
        files=[FileToReview(path="test.py", content="x = 1")],
    )
    result = ReviewResult(request=request, status=ReviewStatus.COMPLETED)

    output_path = tmp_path / "report.json"
    generate_json_report(result, output_path)

    assert output_path.exists()
    parsed = json.loads(output_path.read_text())
    assert parsed["status"] == "completed"
