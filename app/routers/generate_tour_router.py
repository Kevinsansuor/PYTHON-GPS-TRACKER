from fastapi import APIRouter, Depends

from app.security.api_key import require_api_key
from app.models.generate_route import GenerateRouteRequest, GenerateRouteResponse
from app.services.generate_tour_service import GenerateTourService

router = APIRouter()


@router.post(
    "/generate-tour",
    response_model=GenerateRouteResponse,
    dependencies=[Depends(require_api_key)],
    summary="Generar Ruta Óptima para Múltiples Destinos",
)
def generate_tour(request: GenerateRouteRequest):
    """
    Genera una ruta óptima entre dos direcciones utilizando OpenStreetMap.

    **Requiere API Key en el header `X-API-Key`**

    ### Ejemplo:
    ```json
    {
        "origin": "1600 Amphitheatre Parkway, Mountain View, CA",
        "destination": "1 Infinite Loop, Cupertino, CA"
    }
    """
    return GenerateTourService.generate_route(request)
