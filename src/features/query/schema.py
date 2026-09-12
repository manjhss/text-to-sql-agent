from pydantic import BaseModel

# update them, later


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    status: str
