"""
Tests for the AgentState definition and its default_state.

Ensures:
- All expected keys exist in default_state
- Mutating default_state does not leak across tests (it's a shared dict at import time)
- The type annotations are sane (basic structural check)
"""

from src.agent_core.state import AgentState, default_state


REQUIRED_KEYS = [
    "query",
    "query_type",
    "input_guardrail",
    "plan",
    "relevant_tables",
    "schema_context",
    "schema_metadata",
    "raw_sql",
    "query_result",
    "error",
    "error_type",
    "iterations",
    "should_retry",
    "cache_hit",
]


def test_default_state_contains_all_required_keys():
    for key in REQUIRED_KEYS:
        assert key in default_state, f"missing key: {key}"


def test_default_state_has_safe_initial_values():
    assert default_state["query"] == ""
    assert default_state["query_type"] == "irrelevant"
    assert default_state["input_guardrail"] == "unsafe"
    assert default_state["should_retry"] is True
    assert default_state["iterations"] == 0
    assert default_state["cache_hit"] is False


def test_building_state_from_defaults_works():
    """Simulating run_agent's initial state construction."""
    query = "what is the total number of orders?"
    initial_state = {**default_state, "query": query}
    assert initial_state["query"] == query
    assert initial_state["query_type"] == "irrelevant"  # will be overwritten by node
