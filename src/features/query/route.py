from fastapi import APIRouter, HTTPException

from src.agent_core.graph import run_agent
from src.config.logger import logger
from src.features.query.schema import QueryRequest, QueryResponse

router = APIRouter(tags=["agent"])


@router.post("/query", status_code=200, response_model=QueryResponse)
async def query(request: QueryRequest):
    logger.info(f"Query: {request.query}")

    try:
        result = await run_agent(request.query)

        return QueryResponse(
            success=result.get("error") is None,
            plan=result.get("plan"),
            raw_sql=result.get("raw_sql"),
            query_result=result.get("query_result"),
            error=result.get("error"),
            iterations=result.get("iterations", 0),
            cache_hit=result.get("cache_hit", False),
        )
    except Exception as e:
        logger.exception(f"query failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"query processing failed! {str(e)}"
        )
