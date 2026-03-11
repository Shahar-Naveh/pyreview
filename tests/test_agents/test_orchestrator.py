"""Tests for the orchestrator."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pyreview.agents.orchestrator import Orchestrator
from pyreview.core.schemas import ReviewRequest, ReviewStatus


@pytest.mark.asyncio
async def test_orchestrator_runs_all_agents(mock_settings, sample_files):
    """Test that the orchestrator runs all enabled agents and produces a result."""
    request = ReviewRequest(files=sample_files, source="cli")

    # Mock the Anthropic client to return valid responses
    mock_response = MagicMock()
    mock_response.content = [MagicMock()]
    mock_response.content[0].text = '{"findings": [], "summary": "Clean."}'
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 50

    # Synthesis response
    mock_synth = MagicMock()
    mock_synth.content = [MagicMock()]
    mock_synth.content[0].text = '''{
        "overall_score": 8.0,
        "verdict": "approve",
        "executive_summary": "Code looks good.",
        "strengths": ["Clean structure"],
        "top_concerns": [],
        "stats": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    }'''
    mock_synth.usage = MagicMock()
    mock_synth.usage.input_tokens = 200
    mock_synth.usage.output_tokens = 100

    with patch("pyreview.agents.orchestrator.AsyncAnthropic") as MockClient:
        client_instance = AsyncMock()
        # First N calls are agent reviews, last call is synthesis
        client_instance.messages.create = AsyncMock(
            side_effect=[mock_response] * 5 + [mock_synth]
        )
        MockClient.return_value = client_instance

        orchestrator = Orchestrator(mock_settings)
        orchestrator.client = client_instance

        result = await orchestrator.run(request)

    assert result.status == ReviewStatus.COMPLETED
    assert result.summary is not None
    assert result.summary.overall_score == 8.0
    assert result.summary.verdict == "approve"
    assert result.total_execution_time_seconds >= 0


@pytest.mark.asyncio
async def test_orchestrator_deduplicates_findings(mock_settings):
    """Test that overlapping findings are deduplicated."""
    from pyreview.core.schemas import (
        Category,
        CodeLocation,
        Finding,
        Severity,
    )

    orchestrator = Orchestrator(mock_settings)

    findings = [
        Finding(
            agent="security",
            category=Category.SECURITY,
            severity=Severity.CRITICAL,
            title="SQL Injection",
            description="desc1",
            location=CodeLocation(file="app.py", start_line=10),
        ),
        Finding(
            agent="architecture",
            category=Category.SECURITY,
            severity=Severity.HIGH,
            title="Input not validated",
            description="desc2",
            location=CodeLocation(file="app.py", start_line=10),
        ),
    ]

    deduped = orchestrator._deduplicate(findings)
    assert len(deduped) == 1
    assert deduped[0].severity == Severity.CRITICAL
