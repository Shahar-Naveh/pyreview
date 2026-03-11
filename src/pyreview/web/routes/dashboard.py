"""HTML dashboard routes."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["dashboard"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    templates = request.app.state.templates
    store = request.app.state.store
    recent_reviews = await store.list_reviews(limit=20)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "recent_reviews": recent_reviews,
    })


@router.get("/review/{review_id}", response_class=HTMLResponse)
async def review_detail(request: Request, review_id: str):
    templates = request.app.state.templates
    store = request.app.state.store
    review = await store.get_review(review_id)
    return templates.TemplateResponse("review_detail.html", {
        "request": request,
        "review": review,
    })


@router.get("/new", response_class=HTMLResponse)
async def new_review(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse("review_new.html", {
        "request": request,
    })
