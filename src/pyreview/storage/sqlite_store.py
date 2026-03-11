"""SQLite-based persistence for review history."""

from __future__ import annotations

from pathlib import Path

import aiosqlite

from pyreview.core.schemas import ReviewResult
from pyreview.storage.repository import ReviewRepository


class SQLiteStore(ReviewRepository):
    def __init__(self, db_path: str):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    status TEXT NOT NULL,
                    pr_url TEXT,
                    score REAL,
                    verdict TEXT,
                    findings_count INTEGER DEFAULT 0,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            """)
            await db.commit()

    async def save_review(self, result: ReviewResult):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO reviews
                   (id, source, status, pr_url, score, verdict,
                    findings_count, result_json, created_at, completed_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    result.request.id,
                    result.request.source,
                    result.status.value,
                    result.request.pr_url,
                    result.summary.overall_score if result.summary else None,
                    result.summary.verdict if result.summary else None,
                    len(result.all_findings),
                    result.model_dump_json(),
                    result.request.created_at.isoformat(),
                    result.completed_at.isoformat() if result.completed_at else None,
                ),
            )
            await db.commit()

    async def get_review(self, review_id: str) -> ReviewResult | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT result_json FROM reviews WHERE id = ?", (review_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return ReviewResult.model_validate_json(row[0])
                return None

    async def list_reviews(self, limit: int = 50) -> list[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """SELECT id, source, status, pr_url, score, verdict,
                          findings_count, created_at, completed_at
                   FROM reviews ORDER BY created_at DESC LIMIT ?""",
                (limit,),
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
