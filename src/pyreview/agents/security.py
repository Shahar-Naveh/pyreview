"""Security-focused review agent."""

from pyreview.agents.base import BaseAgent
from pyreview.core.schemas import FileToReview


class SecurityAgent(BaseAgent):
    name = "security"
    prompt_file = "security.md"

    def _build_user_message(self, files: list[FileToReview]) -> str:
        parts = ["Review the following Python files for security vulnerabilities:\n"]
        for f in files:
            parts.append(f"### File: {f.path}")
            if f.diff:
                parts.append(f"#### Changes (unified diff):\n```diff\n{f.diff}\n```")
            parts.append(f"#### Full content:\n```python\n{f.content}\n```\n")
        return "\n".join(parts)
