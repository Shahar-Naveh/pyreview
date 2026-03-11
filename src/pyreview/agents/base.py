"""Abstract base class all review agents inherit from."""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from anthropic import AsyncAnthropic

from pyreview.core.schemas import AgentResult, FileToReview, Finding

if TYPE_CHECKING:
    from pyreview.core.config import AgentConfig


class BaseAgent(ABC):
    """
    Each agent:
    1. Has a name and a markdown system prompt in agents/prompts/
    2. Receives file(s) to review
    3. Calls Claude with a structured prompt
    4. Parses Claude's JSON response into Finding objects
    5. Returns an AgentResult
    """

    name: str = "base"
    prompt_file: str = "base.md"

    def __init__(self, client: AsyncAnthropic, config: AgentConfig):
        self.client = client
        self.config = config

    def _load_system_prompt(self) -> str:
        """Load the agent's system prompt from the prompts directory."""
        prompt_path = Path(__file__).parent / "prompts" / self.prompt_file
        return prompt_path.read_text(encoding="utf-8")

    @abstractmethod
    def _build_user_message(self, files: list[FileToReview]) -> str:
        """Subclasses format the file content into a user message."""
        ...

    def _build_response_schema_instructions(self) -> str:
        """JSON schema instruction block appended to the system prompt."""
        return """
You MUST respond with valid JSON matching this exact schema:
{
  "findings": [
    {
      "category": "<security|performance|style|architecture|engineering|bug|best_practice>",
      "severity": "<critical|high|medium|low|info>",
      "title": "<short title>",
      "description": "<detailed explanation>",
      "location": {
        "file": "<file path>",
        "start_line": <int>,
        "end_line": <int or null>
      },
      "fix_suggestion": {
        "description": "<what the fix does>",
        "original_code": "<the problematic code>",
        "suggested_code": "<the corrected code>"
      } or null,
      "confidence": <0.0-1.0>,
      "references": ["<optional URL or standard reference>"]
    }
  ],
  "summary": "<2-3 sentence summary of your analysis>"
}
If there are no findings, return {"findings": [], "summary": "No issues found."}.
Do NOT include any text outside the JSON block.
"""

    async def review(self, files: list[FileToReview]) -> AgentResult:
        """Execute the review pipeline: prompt -> Claude -> parse -> AgentResult."""
        start = time.monotonic()
        system_prompt = (
            self._load_system_prompt()
            + "\n\n"
            + self._build_response_schema_instructions()
        )
        user_message = self._build_user_message(files)

        try:
            response = await self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )

            raw_text = response.content[0].text
            parsed = self._parse_response(raw_text)
            elapsed = time.monotonic() - start

            return AgentResult(
                agent_name=self.name,
                findings=parsed["findings"],
                summary=parsed["summary"],
                execution_time_seconds=round(elapsed, 2),
                token_usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            )
        except Exception as e:
            elapsed = time.monotonic() - start
            return AgentResult(
                agent_name=self.name,
                error=str(e),
                execution_time_seconds=round(elapsed, 2),
            )

    def _parse_response(self, raw: str) -> dict:
        """Parse Claude's JSON response into findings list + summary."""
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]

        data = json.loads(cleaned)

        findings = []
        for f in data.get("findings", []):
            finding = Finding(
                agent=self.name,
                category=f["category"],
                severity=f["severity"],
                title=f["title"],
                description=f["description"],
                location=f["location"],
                fix_suggestion=f.get("fix_suggestion"),
                confidence=f.get("confidence", 0.8),
                references=f.get("references", []),
            )
            findings.append(finding)

        return {
            "findings": findings,
            "summary": data.get("summary", ""),
        }
