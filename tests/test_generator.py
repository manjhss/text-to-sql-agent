"""
Tests for the SQL generator logic (src/agent_core/agents/generator.py).

Covers:
- _clean_sql: markdown stripping / statement detection
- generate(): mocked chain returns valid SQL -> raw_sql emitted
- generate(): missing schema -> returns error (no LLM call)
- REJECTED-sentinel documented as a real bug
"""

import pytest
from unittest.mock import MagicMock, patch

from src.agent_core.agents.generator import SQLGeneratorAgent
from src.agent_core.state import default_state


def _make_mock_chain(response_content):
    """Build a MagicMock that behaves as a runnable chain:
    - supports `prompt | llm_chat` via __or__ returning itself
    - .invoke() returns a response with .content = response_content
    """
    chain = MagicMock()
    resp = MagicMock()
    resp.content = response_content
    chain.invoke.return_value = resp
    chain.__or__ = lambda self, other: chain
    chain.__ror__ = lambda self, other: chain
    return chain


@pytest.fixture
def gen():
    return SQLGeneratorAgent()


# ------------------------------------------------------------------
# _clean_sql behavior
# ------------------------------------------------------------------

def test_clean_sql_strips_markdown(gen):
    assert gen._clean_sql("```sql\nSELECT 1;\n```").startswith("SELECT")


def test_clean_sql_no_markdown(gen):
    assert gen._clean_sql("SELECT COUNT(*) FROM transactions;") == "SELECT COUNT(*) FROM transactions;"


def test_clean_sql_rejects_no_statement(gen):
    with pytest.raises(ValueError, match="No SQL query found"):
        gen._clean_sql("nothing here")


def test_clean_sql_rejected_sentinel_bug(gen):
    """
    BUG: SQL_GENERATION_PROMPT returns 'REJECTED' for destructive plans,
    but _clean_sql only matches SQL keywords → ValueError. The sentinel is lost.
    FIX: add early return in _clean_sql for 'REJECTED'.
    """
    with pytest.raises(ValueError, match="No SQL query found"):
        gen._clean_sql("REJECTED")


# ------------------------------------------------------------------
# generate()
# ------------------------------------------------------------------

def test_generate_returns_sql(gen):
    mock_chain = _make_mock_chain("SELECT COUNT(*) FROM transactions;")
    state = {
        **default_state,
        "query": "how many transactions?",
        "plan": "count all transactions",
        "schema_context": "transactions(transaction_id, order_value)",
    }
    # Patch the generation_prompt so `prompt | llm_chat` yields our mock
    with patch.object(gen, "generation_prompt", MagicMock(__or__=lambda *a: mock_chain)):
        result = gen.generate(state)

    assert "raw_sql" in result, result
    assert result["raw_sql"].startswith("SELECT COUNT(*)")
    mock_chain.invoke.assert_called_once()


def test_generate_strips_markdown(gen):
    mock_chain = _make_mock_chain("```sql\nSELECT 1;\n```")
    state = {**default_state, "query": "x", "plan": "x", "schema_context": "t(id)"}
    with patch.object(gen, "generation_prompt", MagicMock(__or__=lambda *a: mock_chain)):
        result = gen.generate(state)
    assert result["raw_sql"] == "SELECT 1;"


def test_generate_without_schema_returns_error(gen):
    state = {**default_state, "query": "hi", "plan": "x", "schema_context": ""}
    result = gen.generate(state)
    assert result.get("error")
    assert result["should_retry"] is False
