from fastapi import APIRouter

from src.config.logger import logger
from src.features.health.schema import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    try:
        return HealthResponse(status="healthy")
    except Exception as e:
        logger.exception(f"health check failed: {e}")
        return HealthResponse(status="unhealthy")
