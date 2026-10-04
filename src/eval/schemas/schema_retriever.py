from pydantic import BaseModel


class SchemaRetrieverInput(BaseModel):
    query: str
    plan: str


class SchemaRetrieverExpected(BaseModel):
    relevant_tables: list[str]
    schema_context: str


class SchemaRetrieverActual(BaseModel):
    relevant_tables: list[str]
    schema_context: str


class SchemaRetrieverCase(BaseModel):
    id: str
    input: SchemaRetrieverInput
    expected: SchemaRetrieverExpected
    actual: SchemaRetrieverActual
