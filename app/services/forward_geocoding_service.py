"""
Servicio para Forward Geocoding (Dirección → Coordenadas)
"""

from datetime import datetime
from fastapi import HTTPException, status

from app.models.forward_geocoding import ForwardGeocodingResponse
from app.services.geocoding_client import get_geocoding_client


class ForwardGeocodingService:
    """Servicio para convertir direcciones en coordenadas GPS"""

    @staticmethod
    def geocode(address: str) -> ForwardGeocodingResponse:
        """
        Forward Geocoding: Convierte una dirección en coordenadas GPS.

        Args:
            address: Dirección a geocodificar (ej: "Mountain View, CA")

        Returns:
            ForwardGeocodingResponse: Coordenadas y detalles de la ubicación

        Raises:
            HTTPException: Si no se puede geocodificar la dirección
        """
        try:
            client = get_geocoding_client()

            # Intentar con OSM (OpenStreetMap) - gratuito y sin API key
            g = client.osm_geocode(address)

            # Si OSM falla, intentar con ArcGIS
            if not g.ok:
                g = client.arcgis_geocode(address)

            if not g.ok:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se pudo encontrar la dirección: {address}",
                )

            return ForwardGeocodingResponse(
                address=address,
                latitude=g.lat,
                longitude=g.lng,
                formatted_address=g.address,
                city=g.city,
                state=g.state,
                country=g.country,
                postal=g.postal,
                geojson=g.geojson,
                timestamp=datetime.now(),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en forward geocoding: {str(e)}",
            ) from e
