"""
Tests for the Planner agent (src/agent_core/agents/planner.py).

Covers:
- plan_steps extraction via the regex in planner.plan()
- error resilience when the LLM call raises
"""

import pytest
from unittest.mock import MagicMock, patch

from src.agent_core.agents.planner import PlannerAgent, planner_node
from src.agent_core.state import default_state


@pytest.fixture
def planner():
    return PlannerAgent()


def _make_planner_with_mocked_chain(planner, fake_content):
    fake_response = MagicMock()
    fake_response.content = fake_content
    fake_chain = MagicMock()
    fake_chain.invoke.return_value = fake_response
    # planner.plan() calls self.chain.invoke(...) — patch the instance attr
    with patch.object(planner, "chain", fake_chain):
        yield fake_chain


def test_plan_steps_extracts_numbered_lines(planner):
    fake_content = (
        "1. Identify the core intent: aggregation\n"
        "2. Define the metric: total number of orders\n"
        "3. No filters, grouping, or ordering are required."
    )
    fake_chain = MagicMock()
    fake_response = MagicMock()
    fake_response.content = fake_content
    fake_chain.invoke.return_value = fake_response

    with patch.object(planner, "chain", fake_chain):
        result = planner.plan({**default_state, "query": "total orders?"})

    assert "plan" in result
    assert len(result["plan_steps"]) == 3
    assert result["plan_steps"][0].startswith("1.")
    assert result["iterations"] == 0
    assert result["should_retry"] is True


def test_plan_steps_empty_when_no_numbered_lines(planner):
    fake_chain = MagicMock()
    fake_response = MagicMock()
    fake_response.content = "just some prose without numbers"
    fake_chain.invoke.return_value = fake_response

    with patch.object(planner, "chain", fake_chain):
        result = planner.plan({**default_state, "query": "x"})

    assert result["plan_steps"] == []


# --- Error handling ---

def test_plan_handles_llm_failure(planner):
    fake_chain = MagicMock()
    fake_chain.invoke.side_effect = RuntimeError("LLM down")

    with patch.object(planner, "chain", fake_chain):
        result = planner.plan({**default_state, "query": "x"})

    assert result["error"].startswith("planning failed")
    assert result["should_retry"] is False


# --- node wrapper ---

def test_planner_node_wrapper():
    with patch("src.agent_core.agents.planner.PlannerAgent") as MockAgent:
        instance = MockAgent.return_value
        instance.plan.return_value = {
            "plan": "x",
            "plan_steps": ["1. x"],
            "iterations": 0,
            "should_retry": True,
        }
        result = planner_node({**default_state, "query": "hi"})
        assert result["plan"] == "x"
