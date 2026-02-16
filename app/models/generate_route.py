from typing import Optional
from pydantic import BaseModel, Field

class GenerateRouteRequest(BaseModel):
    """Solicitud para generar una ruta entre dos puntos"""
    origin: str = Field(..., description="Dirección de origen", min_length=5)
    destination: str = Field(..., description="Dirección de destino", min_length=5)
    mode: Optional[str] = Field("driving", description="Modo de transporte (driving, walking, bicycling, transit)")
    
class GenerateRouteResponse(BaseModel):
    """Respuesta con detalles de la ruta generada"""
    origin: str = Field(..., description="Dirección de origen")
    destination: str = Field(..., description="Dirección de destino")
    coords: list = Field(..., description="Lista de coordenadas GPS que forman la ruta")