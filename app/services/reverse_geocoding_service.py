"""
Servicio para Reverse Geocoding (Coordenadas → Dirección)
"""

from datetime import datetime
from fastapi import HTTPException, status

from app.models.reverse_geocoding import ReverseGeocodingResponse
from app.services.geocoding_client import get_geocoding_client


class ReverseGeocodingService:
    """Servicio para convertir coordenadas GPS en direcciones"""

    @staticmethod
    def geocode(latitude: float, longitude: float) -> ReverseGeocodingResponse:
        """
        Reverse Geocoding: Convierte coordenadas GPS en una dirección.

        Args:
            latitude: Latitud
            longitude: Longitud

        Returns:
            ReverseGeocodingResponse: Dirección y detalles del lugar

        Raises:
            HTTPException: Si no se puede hacer reverse geocoding
        """
        try:
            client = get_geocoding_client()

            # Intentar con OSM (OpenStreetMap) - gratuito
            g = client.osm_reverse(latitude, longitude)

            # Si OSM falla, intentar con ArcGIS
            if not g.ok:
                g = client.arcgis_reverse(latitude, longitude)

            if not g.ok:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se pudo obtener dirección para las coordenadas: [{latitude}, {longitude}]",
                )

            return ReverseGeocodingResponse(
                latitude=latitude,
                longitude=longitude,
                address=g.address,
                city=g.city,
                state=g.state,
                state_long=g.state_long if hasattr(g, "state_long") else g.state,
                country=g.country,
                country_long=(
                    g.country_long if hasattr(g, "country_long") else g.country
                ),
                postal=g.postal,
                street=g.street,
                timestamp=datetime.now(),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en reverse geocoding: {str(e)}",
            ) from e
