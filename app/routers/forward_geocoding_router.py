"""
Router para Forward Geocoding (Dirección → Coordenadas)
"""

from fastapi import APIRouter, Depends

from app.security.api_key import require_api_key
from app.models.forward_geocoding import (
    ForwardGeocodingRequest,
    ForwardGeocodingResponse,
)
from app.services.forward_geocoding_service import ForwardGeocodingService

router = APIRouter()


@router.post(
    "/forward-geocoding",
    response_model=ForwardGeocodingResponse,
    dependencies=[Depends(require_api_key)],
    summary="Forward Geocoding: Dirección a Coordenadas",
)
def forward_geocoding(request: ForwardGeocodingRequest):
    """
    Convierte una dirección en coordenadas GPS (Forward Geocoding).

    **Requiere API Key en el header `X-API-Key`**

    ### Ejemplo:
    ```json
    {
        "address": "Mountain View, CA"
    }
    ```

    ### Devuelve:
    - Coordenadas GPS (latitud, longitud)
    - Dirección formateada
    - Ciudad, estado, país
    - Código postal
    - Datos GeoJSON
    """
    return ForwardGeocodingService.geocode(request.address)
