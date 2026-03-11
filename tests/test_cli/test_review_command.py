"""Tests for the CLI review command."""

from unittest.mock import AsyncMock, MagicMock, patch

from typer.testing import CliRunner

from pyreview.cli.app import app
from pyreview.core.schemas import (
    FileToReview,
    ReviewRequest,
    ReviewResult,
    ReviewStatus,
    ReviewSummary,
)

runner = CliRunner()


def test_review_no_files(tmp_path):
    """Test review command with empty directory."""
    result = runner.invoke(app, ["review", str(tmp_path)])
    assert result.exit_code == 1
    assert "No Python files found" in result.output


def test_review_command_runs(tmp_path):
    """Test review command with a Python file (mocked orchestrator)."""
    py_file = tmp_path / "test.py"
    py_file.write_text("x = 1\n")

    mock_request = ReviewRequest(
        files=[FileToReview(path=str(py_file), content="x = 1\n")],
        source="cli",
    )
    mock_result = ReviewResult(
        request=mock_request,
        status=ReviewStatus.COMPLETED,
        all_findings=[],
        summary=ReviewSummary(
            overall_score=9.0,
            verdict="approve",
            executive_summary="Clean code.",
        ),
        total_execution_time_seconds=1.5,
        total_token_usage={"input_tokens": 100, "output_tokens": 50},
    )

    with patch("pyreview.cli.commands.review.Orchestrator") as MockOrch:
        instance = MockOrch.return_value
        instance.run = AsyncMock(return_value=mock_result)

        result = runner.invoke(app, ["review", str(py_file)])

    assert result.exit_code == 0
    assert "Reviewing 1 file(s)" in result.output
