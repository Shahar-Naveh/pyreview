"""Tests for the base agent."""

import pytest

from pyreview.agents.security import SecurityAgent
from pyreview.core.schemas import Severity


@pytest.mark.asyncio
async def test_agent_review_returns_findings(
    mock_anthropic_client, mock_agent_config, sample_files
):
    agent = SecurityAgent(client=mock_anthropic_client, config=mock_agent_config)
    result = await agent.review(sample_files)

    assert result.agent_name == "security"
    assert result.error is None
    assert len(result.findings) == 1
    assert result.findings[0].severity == Severity.CRITICAL
    assert result.findings[0].title == "Command Injection"
    assert result.execution_time_seconds >= 0
    assert result.token_usage["input_tokens"] == 500


@pytest.mark.asyncio
async def test_agent_handles_api_error(mock_agent_config, sample_files):
    from unittest.mock import AsyncMock
    from anthropic import AsyncAnthropic

    client = AsyncMock(spec=AsyncAnthropic)
    client.messages.create = AsyncMock(side_effect=Exception("API Error"))

    agent = SecurityAgent(client=client, config=mock_agent_config)
    result = await agent.review(sample_files)

    assert result.agent_name == "security"
    assert result.error == "API Error"
    assert len(result.findings) == 0


@pytest.mark.asyncio
async def test_agent_parses_code_fenced_json(
    mock_anthropic_client, mock_agent_config, sample_files
):
    # Simulate Claude wrapping JSON in code fences
    mock_anthropic_client.messages.create.return_value.content[0].text = '''```json
{
    "findings": [],
    "summary": "No issues found."
}
```'''

    agent = SecurityAgent(client=mock_anthropic_client, config=mock_agent_config)
    result = await agent.review(sample_files)

    assert result.error is None
    assert len(result.findings) == 0
    assert result.summary == "No issues found."
