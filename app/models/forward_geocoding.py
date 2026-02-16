"""
Modelos para Forward Geocoding (Dirección → Coordenadas)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ForwardGeocodingRequest(BaseModel):
    """Solicitud para Forward Geocoding (dirección a coordenadas)"""

    address: str = Field(..., description="Dirección a geocodificar", min_length=3)


class ForwardGeocodingResponse(BaseModel):
    """Respuesta de Forward Geocoding"""

    address: str = Field(..., description="Dirección consultada")
    latitude: float = Field(..., description="Latitud")
    longitude: float = Field(..., description="Longitud")
    formatted_address: Optional[str] = Field(None, description="Dirección formateada")
    city: Optional[str] = Field(None, description="Ciudad")
    state: Optional[str] = Field(None, description="Estado/Provincia")
    country: Optional[str] = Field(None, description="País")
    postal: Optional[str] = Field(None, description="Código postal")
    geojson: Optional[dict] = Field(None, description="Datos GeoJSON")
    department: Optional["DepartmentInfo"] = Field(
        None, description="Información relevante del departamento (Colombia)"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class DepartmentInfo(BaseModel):
    """Información resumida de un departamento en Colombia"""

    name: str = Field(..., description="Nombre del departamento")
    description: Optional[str] = Field(None, description="Descripción corta")
    population: Optional[int] = Field(None, description="Población")
    surface: Optional[int] = Field(None, description="Superficie")
    phone_prefix: Optional[str] = Field(None, description="Prefijo telefónico")
