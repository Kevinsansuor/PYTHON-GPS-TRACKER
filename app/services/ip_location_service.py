"""
Servicio para IP Location
"""

from datetime import datetime
from fastapi import HTTPException, status

from app.models.ip_location import PublicIPLocation
from app.services.geocoding_client import get_geocoding_client


class IPLocationService:
    """Servicio para obtener ubicación GPS desde IP pública"""

    @staticmethod
    def get_location(ip: str = "me") -> PublicIPLocation:
        """
        Obtiene las coordenadas GPS basadas en una IP específica.

        Args:
            ip: Dirección IP a consultar. Por defecto "me" usa la IP actual del cliente.

        Returns:
            PublicIPLocation: Objeto con IP, latitud, longitud y timestamp

        Raises:
            HTTPException: Si no se pueden obtener las coordenadas
        """
        try:
            client = get_geocoding_client()
            location = client.ip_lookup(ip)

            if not location.ok:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="No se pudieron obtener las coordenadas GPS de la IP proporcionada",
                )

            latitude, longitude = location.latlng

            return PublicIPLocation(
                ip=location.ip,
                latitude=latitude,
                longitude=longitude,
                timestamp=datetime.now(),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener ubicación: {str(e)}",
            ) from e
