"""JSON API routes for triggering reviews and retrieving results."""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Request
from pydantic import BaseModel

from pyreview.agents.orchestrator import Orchestrator
from pyreview.core.schemas import FileToReview, ReviewRequest
from pyreview.output.diff_generator import enrich_findings_with_diffs

router = APIRouter(tags=["api"])


class ReviewFilePayload(BaseModel):
    path: str
    content: str


class ReviewRequestPayload(BaseModel):
    files: list[ReviewFilePayload]


class ReviewTriggerResponse(BaseModel):
    review_id: str
    status: str


@router.post("/review", response_model=ReviewTriggerResponse)
async def trigger_review(
    payload: ReviewRequestPayload,
    request: Request,
    background_tasks: BackgroundTasks,
):
    """Submit code for review. Returns immediately; poll for results."""
    settings = request.app.state.settings
    store = request.app.state.store

    files = [
        FileToReview(path=f.path, content=f.content)
        for f in payload.files
    ]
    review_req = ReviewRequest(files=files, source="web")

    background_tasks.add_task(_run_review, settings, store, review_req)

    return ReviewTriggerResponse(
        review_id=review_req.id,
        status="running",
    )


@router.get("/review/{review_id}")
async def get_review(review_id: str, request: Request):
    """Retrieve review results by ID."""
    store = request.app.state.store
    result = await store.get_review(review_id)
    if result:
        return result.model_dump(mode="json")
    return {"status": "not_found"}


@router.get("/reviews")
async def list_reviews(request: Request, limit: int = 50):
    """List recent reviews."""
    store = request.app.state.store
    reviews = await store.list_reviews(limit=limit)
    return reviews


async def _run_review(settings, store, review_req):
    """Background task that runs the orchestrator and stores results."""
    orchestrator = Orchestrator(settings)
    result = await orchestrator.run(review_req)
    result.all_findings = enrich_findings_with_diffs(result.all_findings)
    await store.save_review(result)
