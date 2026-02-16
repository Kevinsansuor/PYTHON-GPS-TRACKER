"""
Router para Health Check
"""

from fastapi import APIRouter
from app.models.base import TrackingResponse

router = APIRouter()


@router.get("/health", response_model=TrackingResponse)
async def health_check():
    """Health check del servicio GPS"""
    return TrackingResponse(
        status="operational",
        message="GPS Tracker API está funcionando correctamente",
        data={"service": "gps_tracker", "version": "1.0.0"},
    )
