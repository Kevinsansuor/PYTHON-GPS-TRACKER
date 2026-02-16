"""
ARCHIVO DEPRECADO - Usar imports desde app.models

Este archivo se mantiene solo para compatibilidad hacia atrás.
Los modelos ahora están modularizados en:
    - app.models.base
    - app.models.ip_location
    - app.models.forward_geocoding
    - app.models.reverse_geocoding
    - app.models.house_address

Usa en su lugar:
    from app.models import (
        GPSLocation,
        TrackingResponse,
        PublicIPLocation,
        ForwardGeocodingRequest,
        ...
    )
"""

# Re-exportar desde los nuevos módulos para compatibilidad
from app.models.base import GPSLocation, TrackingResponse
from app.models.ip_location import IPLocationRequest, PublicIPLocation
from app.models.forward_geocoding import (
    ForwardGeocodingRequest,
    ForwardGeocodingResponse,
)
from app.models.reverse_geocoding import (
    ReverseGeocodingRequest,
    ReverseGeocodingResponse,
)
from app.models.house_address import HouseAddressRequest, HouseAddressResponse

__all__ = [
    "GPSLocation",
    "TrackingResponse",
    "IPLocationRequest",
    "PublicIPLocation",
    "ForwardGeocodingRequest",
    "ForwardGeocodingResponse",
    "ReverseGeocodingRequest",
    "ReverseGeocodingResponse",
    "HouseAddressRequest",
    "HouseAddressResponse",
]
