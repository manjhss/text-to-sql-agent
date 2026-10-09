"""
API layer tests for src/app.py + feature routes.

Tests cover:
- GET /health → 200 {"status": "healthy"}
- POST /query → forwards to run_agent, maps final_state to QueryResponse
- POST /query → on run_agent exception → 500 HTTPException
- POST /query → success path returns expected fields

Uses httpx.AsyncClient + the FastAPI TestClient pattern but with async
support via starlette's TestClient or direct app import with mocking.
"""

import pytest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """A real FastAPI TestClient — no DB/LLM calls reach out because
    run_agent is mocked in each test."""
    from src.app import app
    return TestClient(app)


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------

def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


# ------------------------------------------------------------------
# POST /query
# ------------------------------------------------------------------

def test_query_success(client):
    fake_final_state = {
        "query": "what is the total number of orders?",
        "query_type": "relevant",
        "input_guardrail": "safe",
        "plan": "1. count orders\n2. return total",
        "raw_sql": "SELECT COUNT(*) FROM transactions;",
        "query_result": "Returned 1 row(s). Preview:\nRow 1: {('COUNT(*)', 150000)}",
        "error": None,
        "iterations": 0,
        "cache_hit": False,
    }

    with patch(
        "src.features.query.route.run_agent",
        new_callable=AsyncMock,
        return_value=fake_final_state,
    ):
        resp = client.post("/query", json={"query": "what is the total number of orders?"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["raw_sql"] == "SELECT COUNT(*) FROM transactions;"
    assert body["error"] is None
    assert body["iterations"] == 0


def test_query_failure_returns_500(client):
    with patch(
        "src.features.query.route.run_agent",
        new_callable=AsyncMock,
        side_effect=RuntimeError("boom"),
    ):
        resp = client.post("/query", json={"query": "bad query"})

    assert resp.status_code == 500
    assert "query processing failed" in resp.json()["detail"]


def test_query_rejected_destructive(client):
    # Generator returns REJECTED sentinel → no SQL, error set, success=False
    fake_final_state = {
        "query": "delete all customers",
        "query_type": "relevant",
        "input_guardrail": "safe",
        "plan": "destructive: delete",
        "raw_sql": "REJECTED",
        "query_result": None,
        "error": "destructive database operation",
        "iterations": 0,
        "cache_hit": False,
    }

    with patch(
        "src.features.query.route.run_agent",
        new_callable=AsyncMock,
        return_value=fake_final_state,
    ):
        resp = client.post("/query", json={"query": "delete all customers"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is False
    assert body["raw_sql"] == "REJECTED"
    assert body["error"] == "destructive database operation"


def test_query_validator_runs(client):
    # Confirm the route calls run_agent exactly once with the user's query
    fake_final_state = {**{"query": "x", "error": None, "raw_sql": None, "query_result": None, "iterations": 0, "plan": None, "cache_hit": False}}

    with patch(
        "src.features.query.route.run_agent",
        new_callable=AsyncMock,
        return_value=fake_final_state,
    ) as mock_run:
        client.post("/query", json={"query": "what is the weather?"})
        mock_run.assert_awaited_once_with("what is the weather?")
