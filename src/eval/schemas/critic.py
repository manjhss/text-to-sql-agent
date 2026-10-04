from typing import Any

from pydantic import BaseModel

# validate/execute


class ValidateExecuteInput(BaseModel):
    raw_sql: str


class ValidateExecuteExpected(BaseModel):
    query_result: Any | None = None
    error: str | None = None
    error_type: str | None = None
    should_retry: bool


class ValidateExecuteActual(BaseModel):
    query_result: Any | None = None
    error: str | None = None
    error_type: str | None = None
    should_retry: bool


class ValidateExecuteCase(BaseModel):
    id: str
    input: ValidateExecuteInput
    expected: ValidateExecuteExpected
    actual: ValidateExecuteActual


# reflector


class ReflectorInput(BaseModel):
    raw_query: str
    error: str | None = None
    iterations: int


class ReflectorExpected(BaseModel):
    raw_query: str | None = None
    error: str | None = None
    iterations: int
    should_retry: bool


class ReflectorActual(BaseModel):
    raw_query: str | None = None
    error: str | None = None
    iterations: int
    should_retry: bool


class ReflectorCase(BaseModel):
    id: str
    input: ReflectorInput
    expected: ReflectorExpected
    actual: ReflectorActual
