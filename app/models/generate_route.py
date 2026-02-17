from typing import Optional
from pydantic import BaseModel, Field


class GenerateRouteRequest(BaseModel):
    """Solicitud para generar una ruta entre dos puntos"""

    origin: str = Field(..., description="Dirección de origen", min_length=5)
    destination: str = Field(..., description="Dirección de destino", min_length=5)
    mode: Optional[str] = Field(
        "drive",
        description="Modo de transporte (drive, walk, bike)",
    )


class GenerateRouteResponse(BaseModel):
    """Respuesta con detalles de la ruta generada"""

    origin: str = Field(..., description="Dirección de origen")
    destination: str = Field(..., description="Dirección de destino")
    total_distance_meters: float = Field(..., description="Distancia total en metros")
    estimated_duration_seconds: float = Field(..., description="Tiempo estimado en segundos")
    average_speed_kmh: float = Field(..., description="Velocidad promedio en km/h")
    turn_by_turn_instructions: list = Field(..., description="Instrucciones paso a paso")
    coords: list = Field(..., description="Lista de coordenadas GPS que forman la ruta")
