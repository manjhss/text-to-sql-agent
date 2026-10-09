"""
Tests for the conditional routing functions in src/agent_core/routes/.

These decide the next node in the LangGraph workflow based on the
current AgentState — they are pure functions (mostly) and ideal
candidates for fast, deterministic unit tests.
"""

import pytest

from src.agent_core.routes.intent import route_intent
from src.agent_core.routes.input_guardrail import route_guardrail
from src.agent_core.routes.execution import route_execution
from src.agent_core.state import default_state


class _FakeSettings:
    max_iterations = 3


# ---------- route_intent ----------

def test_route_intent_relevant_continues():
    state = {**default_state, "query": "hi", "query_type": "relevant"}
    assert route_intent(state) == "relevant"


def test_route_intent_irrelevant_stops():
    state = {**default_state, "query": "hi", "query_type": "irrelevant"}
    assert route_intent(state) == "irrelevant"


def test_route_intent_defaults_to_irrelevant():
    # Missing query_type should fall back to irrelevant (fail-safe)
    state = {**default_state, "query": "hi"}
    del state["query_type"]
    assert route_intent(state) == "irrelevant"


# ---------- route_guardrail ----------

def test_route_guardrail_safe_continues():
    state = {**default_state, "query": "hi", "input_guardrail": "safe"}
    assert route_guardrail(state) == "safe"


def test_route_guardrail_unsafe_stops():
    state = {**default_state, "query": "hi", "input_guardrail": "unsafe"}
    assert route_guardrail(state) == "unsafe"


def test_route_guardrail_defaults_to_unsafe():
    state = {**default_state, "query": "hi"}
    del state["input_guardrail"]
    assert route_guardrail(state) == "unsafe"


# ---------- route_execution ----------

@pytest.fixture
def patch_settings(monkeypatch):
    """Override settings.max_iterations without touching the real .env."""
    import src.config.settings as sm
    monkeypatch.setattr(sm, "settings", _FakeSettings(), raising=False)
    yield


def test_route_execution_debugs_on_retry(patch_settings, monkeypatch):
    """When should_retry is True and iterations < max, we should debug."""
    state = {**default_state, "iterations": 0, "should_retry": True}
    assert route_execution(state) == "debug"


def test_route_execution_ends_when_max_iter_reached(patch_settings):
    state = {**default_state, "iterations": 3, "should_retry": True}
    assert route_execution(state) == "end"


def test_route_execution_ends_when_no_retry(patch_settings):
    state = {**default_state, "iterations": 0, "should_retry": False}
    assert route_execution(state) == "end"


def test_route_execution_ends_on_auth_error_like_state(patch_settings):
    """An authorization_error sets should_retry=False, so we end."""
    state = {**default_state, "iterations": 2, "should_retry": False}
    assert route_execution(state) == "end"
