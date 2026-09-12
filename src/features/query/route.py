from fastapi import APIRouter, HTTPException

from src.config.logger import logger
from src.features.query.schema import QueryRequest, QueryResponse

router = APIRouter(tags=["agent"])


@router.get("/query", status_code=200, response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        query = request.query
        # make an agent call here passing query
        return QueryResponse(status="ok")
    except Exception as e:
        logger.exception(f"query failed: {e}")
        raise HTTPException(status_code=500, detail="query processing failed!")
