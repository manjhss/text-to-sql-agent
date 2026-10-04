from pydantic import BaseModel


class GeneratorInput(BaseModel):
    query: str
    plan: str
    schema_context: str


class GeneratorExpected(BaseModel):
    raw_sql: str


class GeneratorActual(BaseModel):
    raw_sql: str


class GeneratorCase(BaseModel):
    id: str
    input: GeneratorInput
    expected: GeneratorExpected
    actual: GeneratorActual
