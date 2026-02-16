"""
Modelos para Forward Geocoding (Dirección → Coordenadas)
"""

from datetime import datetime
from typing import Any, Optional
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
    api_colombia: Optional["ApiColombiaInfo"] = Field(
        None, description="Datos enriquecidos desde API Colombia"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class DepartmentInfo(BaseModel):
    """Información resumida de un departamento en Colombia"""

    id: Optional[int] = Field(None, description="Id del departamento")
    name: str = Field(..., description="Nombre del departamento")
    description: Optional[str] = Field(None, description="Descripción corta")
    population: Optional[int] = Field(None, description="Población")
    surface: Optional[int] = Field(None, description="Superficie")
    phone_prefix: Optional[str] = Field(None, description="Prefijo telefónico")


class ApiColombiaDepartment(BaseModel):
    """Wrapper para informacion del departamento"""

    info: Optional[DepartmentInfo] = Field(None, description="Datos del departamento")


class TouristicAttractionCity(BaseModel):
    """Ciudad asociada a una atraccion turistica"""

    id: Optional[int] = Field(None, description="Id de la ciudad")
    name: Optional[str] = Field(None, description="Nombre de la ciudad")
    description: Optional[str] = Field(None, description="Descripcion")
    surface: Optional[int] = Field(None, description="Superficie")
    population: Optional[int] = Field(None, description="Poblacion")
    postalCode: Optional[str] = Field(None, description="Codigo postal")
    departmentId: Optional[int] = Field(None, description="Id del departamento")
    department: Optional[dict] = Field(None, description="Departamento")
    touristAttractions: Optional[list[Optional[Any]]] = Field(
        None, description="Atracciones asociadas"
    )
    presidents: Optional[Any] = Field(None, description="Presidentes")
    indigenousReservations: Optional[Any] = Field(
        None, description="Reservas indigenas"
    )
    airports: Optional[Any] = Field(None, description="Aeropuertos")
    radios: Optional[Any] = Field(None, description="Radios")


class TouristicAttraction(BaseModel):
    """Atraccion turistica desde API Colombia"""

    id: Optional[int] = Field(None, description="Id")
    name: Optional[str] = Field(None, description="Nombre")
    description: Optional[str] = Field(None, description="Descripcion")
    images: Optional[list[str]] = Field(None, description="Imagenes")
    latitude: Optional[str] = Field(None, description="Latitud")
    longitude: Optional[str] = Field(None, description="Longitud")
    cityId: Optional[int] = Field(None, description="Id de la ciudad")
    city: Optional[TouristicAttractionCity] = Field(None, description="Ciudad")


class ApiColombiaInfo(BaseModel):
    """Estructura para datos de API Colombia"""

    departament: Optional[ApiColombiaDepartment] = Field(
        None, description="Departamento con info"
    )
    touristic: Optional[list[TouristicAttraction]] = Field(
        None, description="Lista de atracciones turisticas"
    )
