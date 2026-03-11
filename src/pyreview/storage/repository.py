"""Abstract storage interface for review history."""

from __future__ import annotations

from abc import ABC, abstractmethod

from pyreview.core.schemas import ReviewResult


class ReviewRepository(ABC):
    """Abstract interface for review persistence."""

    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def save_review(self, result: ReviewResult) -> None: ...

    @abstractmethod
    async def get_review(self, review_id: str) -> ReviewResult | None: ...

    @abstractmethod
    async def list_reviews(self, limit: int = 50) -> list[dict]: ...
