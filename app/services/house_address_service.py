"""
Servicio para House Address (Detalles de Dirección)
"""

from datetime import datetime
from fastapi import HTTPException, status

from app.models.house_address import HouseAddressResponse
from app.services.geocoding_client import get_geocoding_client


class HouseAddressService:
    """Servicio para obtener detalles completos de direcciones"""

    @staticmethod
    def get_details(address: str) -> HouseAddressResponse:
        """
        Obtiene detalles completos de una dirección de casa.

        Args:
            address: Dirección completa (ej: "453 Booth Street, Ottawa ON")

        Returns:
            HouseAddressResponse: Detalles completos de la dirección

        Raises:
            HTTPException: Si no se puede obtener la información
        """
        try:
            client = get_geocoding_client()

            # Intentar con OSM (OpenStreetMap) - gratuito
            g = client.osm_geocode(address)

            # Si OSM falla, intentar con ArcGIS
            if not g.ok:
                g = client.arcgis_geocode(address)

            if not g.ok:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se pudo encontrar la dirección: {address}",
                )

            return HouseAddressResponse(
                address=address,
                latitude=g.lat,
                longitude=g.lng,
                housenumber=g.housenumber if hasattr(g, "housenumber") else None,
                street=g.street,
                street_long=g.street_long if hasattr(g, "street_long") else g.street,
                postal=g.postal,
                city=g.city,
                state=g.state,
                country=g.country,
                formatted_address=g.address,
                timestamp=datetime.now(),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener detalles de dirección: {str(e)}",
            ) from e
