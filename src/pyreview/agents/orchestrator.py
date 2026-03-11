"""Coordinates specialized agents, deduplicates findings, produces synthesis."""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Optional

from anthropic import AsyncAnthropic

from pyreview.agents.architecture import ArchitectureAgent
from pyreview.agents.engineering import EngineeringAgent
from pyreview.agents.performance import PerformanceAgent
from pyreview.agents.security import SecurityAgent
from pyreview.agents.style import StyleAgent
from pyreview.core.schemas import (
    AgentResult,
    ReviewRequest,
    ReviewResult,
    ReviewStatus,
    ReviewSummary,
    Severity,
)

if TYPE_CHECKING:
    from pyreview.core.config import Settings


class Orchestrator:
    """
    Pipeline:
    1. Instantiate enabled agents
    2. Fan-out: run all agents in parallel (asyncio.gather)
    3. Collect AgentResults
    4. Deduplicate overlapping findings
    5. Call Claude once more to synthesize a ReviewSummary
    6. Package everything into a ReviewResult
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncAnthropic(
            api_key=settings.anthropic_api_key.get_secret_value()
        )

    def _build_agents(self) -> list:
        """Instantiate only enabled agents."""
        agent_map = {
            "security": (SecurityAgent, self.settings.security),
            "performance": (PerformanceAgent, self.settings.performance),
            "style": (StyleAgent, self.settings.style),
            "architecture": (ArchitectureAgent, self.settings.architecture),
            "engineering": (EngineeringAgent, self.settings.engineering),
        }
        agents = []
        for name, (cls, cfg) in agent_map.items():
            if cfg.enabled:
                agents.append(cls(client=self.client, config=cfg))
        return agents

    async def run(
        self,
        request: ReviewRequest,
        progress_callback: Optional[Callable[[str, str], None]] = None,
    ) -> ReviewResult:
        """Execute the full review pipeline."""
        overall_start = time.monotonic()
        result = ReviewResult(request=request, status=ReviewStatus.RUNNING)

        agents = self._build_agents()

        # --- Fan-out: run agents in parallel or sequentially ---
        if self.settings.parallel_agents:
            coros = [
                self._run_agent(agent, request, progress_callback)
                for agent in agents
            ]
            agent_results = await asyncio.gather(*coros, return_exceptions=True)
        else:
            agent_results = []
            for agent in agents:
                r = await self._run_agent(agent, request, progress_callback)
                agent_results.append(r)

        # Collect results, handling exceptions from gather
        for ar in agent_results:
            if isinstance(ar, Exception):
                result.agent_results.append(
                    AgentResult(agent_name="unknown", error=str(ar))
                )
            else:
                result.agent_results.append(ar)

        # --- Aggregate all findings ---
        all_findings = []
        for ar in result.agent_results:
            if isinstance(ar, AgentResult):
                all_findings.extend(ar.findings)

        result.all_findings = self._deduplicate(all_findings)

        # --- Synthesize summary via Claude ---
        result.summary = await self._synthesize(result)

        # --- Finalize ---
        result.status = ReviewStatus.COMPLETED
        result.completed_at = datetime.now(timezone.utc)
        result.total_execution_time_seconds = round(
            time.monotonic() - overall_start, 2
        )
        result.total_token_usage = self._sum_tokens(result.agent_results)

        return result

    async def _run_agent(self, agent, request, progress_callback):
        """Run a single agent and optionally report progress."""
        if progress_callback:
            progress_callback(agent.name, "started")
        result = await agent.review(request.files)
        if progress_callback:
            progress_callback(agent.name, "completed")
        return result

    def _deduplicate(self, findings):
        """Remove near-duplicate findings overlapping on the same lines."""
        severity_order = list(Severity)
        seen = {}
        for f in sorted(
            findings,
            key=lambda x: severity_order.index(x.severity)
            if x.severity in severity_order
            else 99,
        ):
            key = (f.location.file, f.location.start_line, f.category)
            if key not in seen:
                seen[key] = f
        return list(seen.values())

    async def _synthesize(self, result: ReviewResult) -> ReviewSummary:
        """Ask Claude to produce a high-level summary from all agent findings."""
        prompt_path = Path(__file__).parent / "prompts" / "orchestrator.md"
        system = prompt_path.read_text(encoding="utf-8")

        findings_json = json.dumps(
            [f.model_dump(mode="json") for f in result.all_findings],
            indent=2,
        )

        user_msg = (
            f"Here are the aggregated findings from {len(result.agent_results)} "
            f"specialized review agents:\n\n{findings_json}\n\n"
            "Produce a JSON synthesis with: overall_score (0-10), verdict "
            "(approve/request_changes/comment), executive_summary, strengths, "
            "top_concerns, and stats (counts by severity)."
        )

        try:
            response = await self.client.messages.create(
                model=self.settings.orchestrator_model,
                max_tokens=2048,
                temperature=0.1,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )

            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1]
                if raw.endswith("```"):
                    raw = raw.rsplit("```", 1)[0]

            data = json.loads(raw)
            return ReviewSummary(**data)
        except Exception:
            # Fallback summary if synthesis fails
            stats = {}
            for f in result.all_findings:
                stats[f.severity.value] = stats.get(f.severity.value, 0) + 1

            total = len(result.all_findings)
            critical = stats.get("critical", 0)
            high = stats.get("high", 0)

            if critical > 0:
                score, verdict = 2.0, "request_changes"
            elif high > 0:
                score, verdict = 5.0, "comment"
            elif total > 5:
                score, verdict = 6.0, "comment"
            else:
                score, verdict = 8.0, "approve"

            return ReviewSummary(
                overall_score=score,
                verdict=verdict,
                executive_summary=f"Review found {total} issues across {len(result.agent_results)} agents.",
                stats=stats,
            )

    def _sum_tokens(self, agent_results):
        """Sum token usage across all agents."""
        total = {"input_tokens": 0, "output_tokens": 0}
        for ar in agent_results:
            if isinstance(ar, AgentResult):
                for k, v in ar.token_usage.items():
                    total[k] = total.get(k, 0) + v
        return total
