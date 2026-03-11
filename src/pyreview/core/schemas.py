"""Pydantic models defining the review data contract across the entire system."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------- Enums ----------

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Category(str, Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    ARCHITECTURE = "architecture"
    ENGINEERING = "engineering"
    BUG = "bug"
    BEST_PRACTICE = "best_practice"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# ---------- Input Models ----------

class FileToReview(BaseModel):
    """A single file presented for review."""
    path: str
    content: str
    language: str = "python"
    diff: Optional[str] = None


class ReviewRequest(BaseModel):
    """Top-level input to the review pipeline."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    files: list[FileToReview]
    source: str = "cli"
    pr_url: Optional[str] = None
    pr_number: Optional[int] = None
    repo_full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------- Finding Models ----------

class CodeLocation(BaseModel):
    """Precise location in source code."""
    file: str
    start_line: int
    end_line: Optional[int] = None
    column: Optional[int] = None


class FixSuggestion(BaseModel):
    """A concrete code fix with before/after and unified diff."""
    description: str
    original_code: str
    suggested_code: str
    diff: str = ""


class Finding(BaseModel):
    """A single review finding produced by an agent."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    agent: str
    category: Category
    severity: Severity
    title: str
    description: str
    location: CodeLocation
    fix_suggestion: Optional[FixSuggestion] = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    references: list[str] = Field(default_factory=list)


# ---------- Agent Result ----------

class AgentResult(BaseModel):
    """Output of a single specialized agent."""
    agent_name: str
    findings: list[Finding] = Field(default_factory=list)
    summary: str = ""
    execution_time_seconds: float = 0.0
    token_usage: dict[str, int] = Field(default_factory=dict)
    error: Optional[str] = None


# ---------- Review Result ----------

class ReviewSummary(BaseModel):
    """High-level summary produced by the orchestrator."""
    overall_score: float = Field(ge=0.0, le=10.0)
    verdict: str
    executive_summary: str
    strengths: list[str] = Field(default_factory=list)
    top_concerns: list[str] = Field(default_factory=list)
    stats: dict[str, int] = Field(default_factory=dict)


class ReviewResult(BaseModel):
    """Complete output of the review pipeline."""
    request: ReviewRequest
    agent_results: list[AgentResult] = Field(default_factory=list)
    all_findings: list[Finding] = Field(default_factory=list)
    summary: Optional[ReviewSummary] = None
    status: ReviewStatus = ReviewStatus.PENDING
    completed_at: Optional[datetime] = None
    total_execution_time_seconds: float = 0.0
    total_token_usage: dict[str, int] = Field(default_factory=dict)
