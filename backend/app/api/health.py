"""
Health check endpoints
"""
import logging
from fastapi import APIRouter, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    environment: str


@router.get(
    "/",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment="production"
    )


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe"
)
async def liveness_probe():
    """Kubernetes liveness probe"""
    return {"status": "alive"}


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe"
)
async def readiness_probe():
    """Kubernetes readiness probe"""
    return {"status": "ready"}
