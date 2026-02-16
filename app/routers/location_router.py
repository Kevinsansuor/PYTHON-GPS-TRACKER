"""
ARCHIVO DEPRECADO - No usar este router

Este archivo se mantiene solo para compatibilidad hacia atrás.
Los routers ahora están modularizados en:
    - app.routers.health_router
    - app.routers.ip_location_router
    - app.routers.forward_geocoding_router
    - app.routers.reverse_geocoding_router
    - app.routers.house_address_router

Los endpoints son registrados directamente en main.py usando los routers modulares.
"""

from fastapi import APIRouter

# Router vacío para compatibilidad - NO USAR
router = APIRouter()

# Este router ya no contiene endpoints
# Todos los endpoints están ahora en los routers modulares
