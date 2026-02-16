"""
Router para Reverse Geocoding (Coordenadas → Dirección)
"""

from fastapi import APIRouter, Depends

from app.security.api_key import require_api_key
from app.models.reverse_geocoding import (
    ReverseGeocodingRequest,
    ReverseGeocodingResponse,
)
from app.services.reverse_geocoding_service import ReverseGeocodingService

router = APIRouter()


@router.post(
    "/reverse-geocoding",
    response_model=ReverseGeocodingResponse,
    dependencies=[Depends(require_api_key)],
    summary="Reverse Geocoding: Coordenadas a Dirección",
)
def reverse_geocoding(request: ReverseGeocodingRequest):
    """
    Convierte coordenadas GPS en una dirección (Reverse Geocoding).

    **Requiere API Key en el header `X-API-Key`**

    ### Ejemplo:
    ```json
    {
        "latitude": 45.15,
        "longitude": -75.14
    }
    ```

    ### Devuelve:
    - Dirección completa
    - Ciudad, estado (completo y abreviado)
    - País (código y nombre completo)
    - Código postal
    - Nombre de calle
    """
    return ReverseGeocodingService.geocode(request.latitude, request.longitude)
