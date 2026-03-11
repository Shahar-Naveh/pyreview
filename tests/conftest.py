"""Shared test fixtures for pyreview tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from pyreview.core.config import AgentConfig, Settings
from pyreview.core.schemas import FileToReview


@pytest.fixture
def sample_file() -> FileToReview:
    return FileToReview(
        path="test_sample.py",
        content='''import os

def run_command(user_input):
    """Execute a command from user input."""
    os.system(user_input)  # Security issue: command injection

def calculate_forces(forces):
    """Sum forces in a system."""
    total = [0, 0, 0]
    for f in forces:
        for i in range(3):
            total[i] += f[i]  # Performance: should use numpy
    return total

class DataProcessor:
    def process(self, data):
        result = []
        for item in data:
            if item > 0:
                if item < 100:
                    if item != 50:
                        result.append(item * 2)
        return result
''',
        language="python",
    )


@pytest.fixture
def sample_files(sample_file) -> list[FileToReview]:
    return [sample_file]


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(
        anthropic_api_key="sk-ant-test-key-for-testing",
        github_token=None,
        default_model="claude-sonnet-4-5-20250929",
        parallel_agents=False,
    )


@pytest.fixture
def mock_agent_config() -> AgentConfig:
    return AgentConfig(
        enabled=True,
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        temperature=0.2,
    )


@pytest.fixture
def mock_anthropic_client():
    """Mock AsyncAnthropic client that returns a valid JSON response."""
    client = AsyncMock()
    response = MagicMock()
    response.content = [MagicMock()]
    response.content[0].text = '''{
        "findings": [
            {
                "category": "security",
                "severity": "critical",
                "title": "Command Injection",
                "description": "os.system() with user input allows arbitrary command execution",
                "location": {
                    "file": "test_sample.py",
                    "start_line": 5,
                    "end_line": 5
                },
                "fix_suggestion": {
                    "description": "Use subprocess.run with shell=False",
                    "original_code": "os.system(user_input)",
                    "suggested_code": "subprocess.run(shlex.split(user_input), check=True)"
                },
                "confidence": 0.95,
                "references": ["CWE-78"]
            }
        ],
        "summary": "Found 1 critical security issue: command injection via os.system()."
    }'''
    response.usage = MagicMock()
    response.usage.input_tokens = 500
    response.usage.output_tokens = 200
    client.messages.create = AsyncMock(return_value=response)
    return client
