"""
Servicio para Forward Geocoding (Dirección → Coordenadas)
"""

from datetime import datetime
import unicodedata
from typing import Optional
from fastapi import HTTPException, status

from app.models.forward_geocoding import DepartmentInfo, ForwardGeocodingResponse
from app.services.geocoding_client import get_geocoding_client


class ForwardGeocodingService:
    """Servicio para convertir direcciones en coordenadas GPS"""

    @staticmethod
    def _normalize_text(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value)
        return "".join(ch for ch in normalized if not unicodedata.combining(ch)).lower()

    @staticmethod
    def _shorten(text: str, max_len: int = 310) -> str:
        if len(text) <= max_len:
            return text
        return text[: max_len - 3].rstrip() + "..."

    @classmethod
    def _get_department_info(
        cls, client, state: Optional[str], country: Optional[str]
    ) -> Optional[DepartmentInfo]:
        if not state or not country:
            return None

        country_norm = cls._normalize_text(country)
        if country_norm not in {"colombia", "co"}:
            return None

        departments = client.colombia_departments()
        if not departments:
            return None

        state_norm = cls._normalize_text(state)
        for dept in departments:
            name = dept.get("name")
            if not name:
                continue
            if cls._normalize_text(name) == state_norm:
                description = dept.get("description")
                if isinstance(description, str):
                    description = cls._shorten(description)
                return DepartmentInfo(
                    name=name,
                    description=description,
                    population=dept.get("population"),
                    surface=dept.get("surface"),
                    phone_prefix=dept.get("phonePrefix"),
                )
        return None

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

            department_info = ForwardGeocodingService._get_department_info(
                client, g.state, g.country
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
                department=department_info,
                timestamp=datetime.now(),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en forward geocoding: {str(e)}",
            ) from e
