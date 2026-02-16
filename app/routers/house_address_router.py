"""
Router para House Address (Detalles de Dirección)
"""

from fastapi import APIRouter, Depends

from app.security.api_key import require_api_key
from app.models.house_address import HouseAddressRequest, HouseAddressResponse
from app.services.house_address_service import HouseAddressService

router = APIRouter()


@router.post(
    "/house-address",
    response_model=HouseAddressResponse,
    dependencies=[Depends(require_api_key)],
    summary="Detalles de Dirección de Casa",
)
def get_house_address(request: HouseAddressRequest):
    """
    Obtiene detalles completos de una dirección de casa específica.

    **Requiere API Key en el header `X-API-Key`**

    ### Ejemplo:
    ```json
    {
        "address": "453 Booth Street, Ottawa ON"
    }
    ```

    ### Devuelve:
    - Número de casa
    - Calle (abreviado y completo)
    - Código postal
    - Ciudad, estado, país
    - Coordenadas GPS
    - Dirección formateada
    """
    return HouseAddressService.get_details(request.address)
