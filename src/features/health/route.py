from fastapi import APIRouter, HTTPException

from src.config.logger import logger
from src.features.health.schema import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", status_code=200, response_model=HealthResponse)
def health_check():
    try:
        return HealthResponse(status="healthy")
    except Exception as e:
        logger.exception(f"health check failed: {e}")
        raise HTTPException(status_code=500, detail="health check failed!")
