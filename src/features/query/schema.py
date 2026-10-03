from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    success: bool
    raw_sql: Optional[str] = None
    query_result: Optional[str] = None
    error: Optional[str] = None
    iterations: int = 0
    cache_hit: bool = False
    plan: Optional[str] = None
