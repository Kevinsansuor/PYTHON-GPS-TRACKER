from datetime import datetime
from fastapi import HTTPException, status
import osmnx as ox
import networkx as nx

from app.models.generate_route import GenerateRouteRequest, GenerateRouteResponse
from app.services.geocoding_client import get_geocoding_client

class GenerateTourService:
    """Servicio para generar una ruta entre dos direcciones"""
    
    @staticmethod
    def generate_route(request: GenerateRouteRequest) -> GenerateRouteResponse:
        """
        Docstring para generate_route
        
        :param request: Descripción
        :type request: GenerateRouteRequest
        :return: Descripción
        :rtype: GenerateRouteResponse
        """
        try:
            client = get_geocoding_client()
            
            origin = client.osm_geocode(request.origin)
            destination = client.osm_geocode(request.destination)
            
            if not origin.ok:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se pudo encontrar la dirección de origen: {request.origin}",
                )

            if not destination.ok:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se pudo encontrar la dirección de destino: {request.destination}",
                )
            
            
            center = (
                (origin.lat + destination.lat) / 2,
                (origin.lng + destination.lng) / 2,
            )
            
            print(f"Generando grafo alrededor del centro: {center}")
            
            G = ox.graph_from_point(center, dist=15000, network_type="drive")
            
            print(f"Grafo generado con {len(G.nodes)} nodos y {len(G.edges)} aristas")
            
            origin_node = ox.distance.nearest_nodes(G, origin.lng, origin.lat)
            destination_node = ox.distance.nearest_nodes(G, destination.lng, destination.lat)
            
            G = ox.project_graph(G)
            print("Grafo proyectado a CRS UTM")
            
            route = nx.shortest_path(G, origin_node, destination_node, weight="length")
            
            print(f"Ruta generada con {len(route)} nodos")
            
            G_latlng = ox.project_graph(G, to_crs="EPSG:4326")
            
            coords = [
                (G_latlng.nodes[node]["y"], G_latlng.nodes[node]["x"])
                for node in route
            ]
            
            print(f"Coordenadas de la ruta: {coords}")
            
            return GenerateRouteResponse(
                origin=request.origin,
                destination=request.destination,
                coords=coords,
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar la ruta: {str(e)}",
            ) from e