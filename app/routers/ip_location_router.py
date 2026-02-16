"""
Router para IP Location
"""

from fastapi import APIRouter, Request, Depends

from app.security.api_key import require_api_key
from app.models.ip_location import IPLocationRequest, PublicIPLocation
from app.services.ip_location_service import IPLocationService

router = APIRouter()


@router.post(
    "/my-location",
    response_model=PublicIPLocation,
    dependencies=[Depends(require_api_key)],
)
def get_my_location(request: Request, location_request: IPLocationRequest):
    """
    Obtiene la ubicación GPS basada en una IP.

    **Requiere API Key en el header `X-API-Key`**

    - Si se proporciona `ip` en el body, busca la geolocalización de esa IP
    - Si no se proporciona, usa la IP del cliente que realiza la solicitud

    Args:
        location_request: Objeto con la IP (opcional)

    Returns:
        PublicIPLocation: Coordenadas GPS de la IP consultada
    """
    ip_to_check = location_request.ip if location_request.ip else request.client.host
    return IPLocationService.get_location(ip_to_check)
