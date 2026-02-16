"""
Modelos base compartidos
"""

from typing import Optional
from pydantic import BaseModel, Field


class GPSLocation(BaseModel):
    """Modelo para una ubicación GPS"""

    latitude: float = Field(..., description="Latitud")
    longitude: float = Field(..., description="Longitud")
    timestamp: Optional[str] = Field(None, description="Fecha/hora de la ubicación")


class TrackingResponse(BaseModel):
    """Modelo de respuesta del servicio"""

    status: str = Field(..., description="Estado de la operación")
    message: str = Field(..., description="Mensaje de respuesta")
    data: Optional[dict] = Field(None, description="Datos adicionales")
