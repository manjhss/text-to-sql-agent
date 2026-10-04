from pydantic import BaseModel


class PlannerInput(BaseModel):
    query: str


class PlannerExpected(BaseModel):
    plan: str


class PlannerActual(BaseModel):
    plan: str


class PlannerCase(BaseModel):
    id: str
    input: PlannerInput
    expected: PlannerExpected
    actual: PlannerActual
