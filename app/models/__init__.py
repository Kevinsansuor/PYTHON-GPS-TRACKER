"""
Modelos de la aplicación GPS Tracker
"""

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

from app.models.generate_route import GenerateRouteRequest, GenerateRouteResponse

__all__ = [
    # Base
    "GPSLocation",
    "TrackingResponse",
    # IP Location
    "IPLocationRequest",
    "PublicIPLocation",
    # Forward Geocoding
    "ForwardGeocodingRequest",
    "ForwardGeocodingResponse",
    # Reverse Geocoding
    "ReverseGeocodingRequest",
    "ReverseGeocodingResponse",
    # House Address
    "HouseAddressRequest",
    "HouseAddressResponse",
    # Generate Route
    "GenerateRouteRequest",
    "GenerateRouteResponse",
]
