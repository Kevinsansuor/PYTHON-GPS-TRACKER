"""
Modelos para Reverse Geocoding (Coordenadas → Dirección)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReverseGeocodingRequest(BaseModel):
    """Solicitud para Reverse Geocoding (coordenadas a dirección)"""

    latitude: float = Field(..., description="Latitud", ge=-90, le=90)
    longitude: float = Field(..., description="Longitud", ge=-180, le=180)


class ReverseGeocodingResponse(BaseModel):
    """Respuesta de Reverse Geocoding"""

    latitude: float = Field(..., description="Latitud consultada")
    longitude: float = Field(..., description="Longitud consultada")
    address: Optional[str] = Field(None, description="Dirección completa")
    city: Optional[str] = Field(None, description="Ciudad")
    state: Optional[str] = Field(None, description="Estado/Provincia (abreviado)")
    state_long: Optional[str] = Field(None, description="Estado/Provincia (completo)")
    country: Optional[str] = Field(None, description="País (código)")
    country_long: Optional[str] = Field(None, description="País (nombre completo)")
    postal: Optional[str] = Field(None, description="Código postal")
    street: Optional[str] = Field(None, description="Calle")
    timestamp: datetime = Field(default_factory=datetime.now)
