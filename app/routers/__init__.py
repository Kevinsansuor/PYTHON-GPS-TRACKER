"""
Routers de la aplicación GPS Tracker
"""

from app.routers import (
    health_router,
    ip_location_router,
    forward_geocoding_router,
    reverse_geocoding_router,
    house_address_router,
    cache_router,
)

__all__ = [
    "health_router",
    "ip_location_router",
    "forward_geocoding_router",
    "reverse_geocoding_router",
    "house_address_router",
    "cache_router",
]
