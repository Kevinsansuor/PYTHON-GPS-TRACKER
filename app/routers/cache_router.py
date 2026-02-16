"""
Router para administracion de cache
"""

from fastapi import APIRouter, Depends

from app.security.api_key import require_api_key
from app.services.geocoding_client import clear_geocoding_cache

router = APIRouter()


@router.post(
    "/cache/clear",
    dependencies=[Depends(require_api_key)],
    summary="Limpiar cache en memoria",
)
def clear_cache():
    """
    Limpia el cache en memoria del cliente de geocoding.

    **Requiere API Key en el header `X-API-Key`**
    """
    clear_geocoding_cache()
    return {"status": "ok", "message": "Cache limpiado"}
