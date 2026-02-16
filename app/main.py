"""
Aplicación principal de GPS Tracker API con FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.configs.config

from app.routers import (
    forward_geocoding_router,
    health_router,
    house_address_router,
    ip_location_router,
    reverse_geocoding_router,
    cache_router,
    generate_tour_router,
)

app = FastAPI(
    title="GPS Tracker API",
    version="1.0.0",
    description="API de seguimiento GPS y geocoding",
    docs_url="/api/gps/docs",
    redoc_url="/api/gps/redoc",
    openapi_url="/api/gps/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    """
    Health check principal de la API.
    """
    return {"status": "ok"}


app.include_router(
    health_router.router,
    prefix="/api/gps",
    tags=["health"],
)

app.include_router(
    ip_location_router.router,
    prefix="/api/gps",
    tags=["ip-location"],
)

app.include_router(
    forward_geocoding_router.router,
    prefix="/api/gps",
    tags=["forward-geocoding"],
)

app.include_router(
    reverse_geocoding_router.router,
    prefix="/api/gps",
    tags=["reverse-geocoding"],
)

app.include_router(
    house_address_router.router,
    prefix="/api/gps",
    tags=["house-address"],
)

app.include_router(
    generate_tour_router.router,
    prefix="/api/gps",
    tags=["generate-tour"],
)

app.include_router(
    cache_router.router,
    prefix="/api/gps",
    tags=["admin"],
)
