"""
Modelos para IP Location
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IPLocationRequest(BaseModel):
    """Modelo para solicitud de ubicación por IP"""

    ip: Optional[str] = Field(
        None,
        description="Dirección IP a consultar (opcional, usa la actual si no se proporciona)",
    )


class PublicIPLocation(BaseModel):
    """Modelo para ubicación basada en IP pública"""

    ip: str = Field(..., description="Dirección IP pública")
    latitude: float = Field(..., description="Latitud obtenida desde IP")
    longitude: float = Field(..., description="Longitud obtenida desde IP")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp de obtención"
    )
