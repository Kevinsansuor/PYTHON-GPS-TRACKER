"""
Modelos para House Address (Detalles de Dirección)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HouseAddressRequest(BaseModel):
    """Solicitud para obtener detalles de dirección de casa"""

    address: str = Field(..., description="Dirección completa de la casa", min_length=5)


class HouseAddressResponse(BaseModel):
    """Respuesta con detalles de dirección de casa"""

    address: str = Field(..., description="Dirección consultada")
    latitude: float = Field(..., description="Latitud")
    longitude: float = Field(..., description="Longitud")
    housenumber: Optional[str] = Field(None, description="Número de casa")
    street: Optional[str] = Field(None, description="Calle (abreviado)")
    street_long: Optional[str] = Field(None, description="Calle (completo)")
    postal: Optional[str] = Field(None, description="Código postal")
    city: Optional[str] = Field(None, description="Ciudad")
    state: Optional[str] = Field(None, description="Estado/Provincia")
    country: Optional[str] = Field(None, description="País")
    formatted_address: Optional[str] = Field(None, description="Dirección formateada")
    timestamp: datetime = Field(default_factory=datetime.now)
