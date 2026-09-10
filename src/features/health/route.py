from fastapi import APIRouter

from src.features.health.schema import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    try:
        return HealthResponse(status="healthy")
    except Exception as e:
        print(f"health check failed: {e}")
        return HealthResponse(status="unhealthy")
