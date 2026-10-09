"""
Shared pytest fixtures for Text-to-SQL Agent tests.
No real external services (DB / LLM / TypeSafe) are used — everything
is either in-memory or mocked downstream.
"""

import sys
from pathlib import Path

# Ensure repo root is importable so `src.*` works under pytest
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch):
    """Point settings at an in-memory SQLite DB so tests never touch disk."""
    monkeypatch.setenv("DATABASE_URI", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")
    monkeypatch.setenv("JEV_API_KEY", "test-jev-key")
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "8000")
    yield
