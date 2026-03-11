"""FastAPI application factory for the web dashboard."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pyreview.core.config import Settings
from pyreview.storage.sqlite_store import SQLiteStore
from pyreview.web.routes import api, dashboard, ws

WEB_DIR = Path(__file__).parent


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = Settings.from_yaml(Path("config.yaml"))

    app = FastAPI(title="pyreview Dashboard", version="0.1.0")

    # Mount static files
    app.mount(
        "/static",
        StaticFiles(directory=str(WEB_DIR / "static")),
        name="static",
    )

    # Jinja2 templates
    templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))

    # Storage
    store = SQLiteStore(settings.db_path)

    # Store in app state
    app.state.settings = settings
    app.state.templates = templates
    app.state.store = store

    # Initialize DB on startup
    @app.on_event("startup")
    async def startup():
        await store.initialize()

    # Register routes
    app.include_router(dashboard.router)
    app.include_router(api.router, prefix="/api")
    app.include_router(ws.router)

    return app
