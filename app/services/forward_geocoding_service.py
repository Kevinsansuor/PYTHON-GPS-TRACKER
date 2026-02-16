"""
Servicio para Forward Geocoding (Dirección → Coordenadas)
"""

from datetime import datetime
import unicodedata
from typing import Optional
from fastapi import HTTPException, status

from app.models.forward_geocoding import (
    ApiColombiaDepartment,
    ApiColombiaInfo,
    DepartmentInfo,
    ForwardGeocodingResponse,
    TouristicAttraction,
)
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
                    id=dept.get("id"),
                    name=name,
                    description=description,
                    population=dept.get("population"),
                    surface=dept.get("surface"),
                    phone_prefix=dept.get("phonePrefix"),
                )
        return None

    @classmethod
    def _filter_touristic_attractions(
        cls, attractions: Optional[list[dict]], department_id: Optional[int]
    ) -> list[TouristicAttraction]:
        if not attractions or not department_id:
            return []

        results: list[TouristicAttraction] = []
        for attraction in attractions:
            city = attraction.get("city") if isinstance(attraction, dict) else None
            if not isinstance(city, dict):
                continue
            if city.get("departmentId") != department_id:
                continue
            results.append(TouristicAttraction(**attraction))
        return results

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

            touristic_list: list[TouristicAttraction] = []
            if department_info and department_info.id:
                attractions = client.colombia_touristic_attractions()
                touristic_list = ForwardGeocodingService._filter_touristic_attractions(
                    attractions, department_info.id
                )

            api_colombia = ApiColombiaInfo(
                departament=ApiColombiaDepartment(info=department_info),
                touristic=touristic_list,
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
                api_colombia=api_colombia,
                timestamp=datetime.now(),
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en forward geocoding: {str(e)}",
            ) from e
