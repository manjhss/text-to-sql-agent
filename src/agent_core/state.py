from typing import Any, Optional, TypedDict


class AgentState(TypedDict):
    """
    state that flows through the agent graph and maintains all the required context
    """

    # input
    query: str  # original user query

    # planning phase
    plan: Optional[str]  # high-level logical plan

    # schema retrieval phase
    relevant_tables: Optional[list[str]]  # selected table names
    schema_context: Optional[str]  # schema info for relevant tables
    schema_metadata: Optional[dict[str, Any]]  # additional metadata

    # generation phase
    raw_sql: Optional[str]  # generated raw sql

    # execution phase
    query_result: Optional[Any]  # execution result

    # error handling
    error: Optional[str]  # error message if execution failed
    error_type: Optional[str]  # type of error (syntax, runtime, logic)

    # control flow
    iterations: int  # number of correction attempts
    should_retry: bool  # whether to attempt correction

    # metadata
    cache_hit: Optional[bool]  # whether result came from cache
