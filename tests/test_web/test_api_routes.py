"""Tests for the web API routes."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from fastapi.testclient import TestClient

from pyreview.core.config import Settings
from pyreview.storage.sqlite_store import SQLiteStore
from pyreview.web.app import create_app


@pytest.fixture
def client(tmp_path):
    settings = Settings(
        anthropic_api_key="test-key",
        db_path=str(tmp_path / "test_reviews.db"),
    )
    app = create_app(settings)

    # Use TestClient which triggers startup events
    with TestClient(app) as c:
        yield c


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "pyreview" in response.text


def test_new_review_page_loads(client):
    response = client.get("/new")
    assert response.status_code == 200
    assert "Submit Code for Review" in response.text


def test_api_list_reviews(client):
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert response.json() == []
