from typing import Any

from pydantic import BaseModel


class AgentExpected(BaseModel):
    raw_sql: str
    query_result: Any
    error: str | None = None
    iterations: int


class AgentActual(BaseModel):
    raw_sql: str
    query_result: Any
    error: str | None = None
    iterations: int


class AgentCase(BaseModel):
    id: str
    question: str
    expected: AgentExpected
    actual: AgentActual
