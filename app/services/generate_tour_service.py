from fastapi import HTTPException, status
import osmnx as ox
import networkx as nx
from shapely.geometry import LineString
from app.models.generate_route import GenerateRouteRequest, GenerateRouteResponse
from app.services.geocoding_client import get_geocoding_client


class GenerateTourService:

    OSMNX_MODES = {
        "driving": "drive",
        "walking": "walk",
        "bicycling": "bike",
    }

    @staticmethod
    def _generate_turn_by_turn(G, route_nodes):
        """Genera instrucciones paso a paso para la ruta"""
        instructions = []
        accumulated_distance = 0
        current_street = None
        segment_distance = 0

        for i, (u, v) in enumerate(zip(route_nodes[:-1], route_nodes[1:])):
            edge = G[u][v][0]
            distance = edge.get("length", 0)
            street_name = edge.get("name", "Calle sin nombre")

            if isinstance(street_name, list):
                street_name = street_name[0] if street_name else "Calle sin nombre"

            if current_street is None:
                current_street = street_name
                instructions.append(
                    {
                        "instruction": f"Inicia en {street_name}",
                        "distance_meters": 0,
                        "street_name": street_name,
                    }
                )

            elif street_name != current_street:
                instructions.append(
                    {
                        "instruction": f"Continúa por {current_street} durante {int(segment_distance)}m",
                        "distance_meters": round(accumulated_distance, 0),
                        "street_name": current_street,
                    }
                )
                instructions.append(
                    {
                        "instruction": f"Gira hacia {street_name}",
                        "distance_meters": round(
                            accumulated_distance + segment_distance, 0
                        ),
                        "street_name": street_name,
                    }
                )
                accumulated_distance += segment_distance
                segment_distance = 0
                current_street = street_name

            segment_distance += distance

        if segment_distance > 0:
            instructions.append(
                {
                    "instruction": f"Continúa por {current_street} durante {int(segment_distance)}m",
                    "distance_meters": round(accumulated_distance, 0),
                    "street_name": current_street,
                }
            )

        instructions.append(
            {
                "instruction": "Has llegado a tu destino",
                "distance_meters": round(accumulated_distance + segment_distance, 0),
                "street_name": "",
            }
        )

        return instructions

    @staticmethod
    def generate_route(request: GenerateRouteRequest) -> GenerateRouteResponse:
        try:
            ox.settings.max_query_area_size = 2500000000  # 50km x 50km
            ox.settings.use_cache = True

            client = get_geocoding_client()
            origin_loc = client.osm_geocode(request.origin)
            dest_loc = client.osm_geocode(request.destination)

            if not origin_loc.ok or not dest_loc.ok:
                raise HTTPException(status_code=404, detail="Dirección no encontrada")

            center_lat = (origin_loc.lat + dest_loc.lat) / 2
            center_lng = (origin_loc.lng + dest_loc.lng) / 2

            dist_meters = ox.distance.great_circle(
                origin_loc.lat, origin_loc.lng, dest_loc.lat, dest_loc.lng
            )

            radius = (dist_meters / 2) + 1000

            print(
                f"Generando grafo desde ({center_lat}, {center_lng}) con radio de {int(radius)}m"
            )

            network_type = GenerateTourService.OSMNX_MODES.get(request.mode, "drive")

            G = ox.graph_from_point(
                (center_lat, center_lng), dist=radius, network_type=network_type
            )

            G = ox.add_edge_speeds(G)
            G = ox.add_edge_travel_times(G)

            origin_node = ox.distance.nearest_nodes(G, origin_loc.lng, origin_loc.lat)
            dest_node = ox.distance.nearest_nodes(G, dest_loc.lng, dest_loc.lat)

            G_proj = ox.project_graph(G)

            def heuristic(u, v):
                x1, y1 = G_proj.nodes[u]["x"], G_proj.nodes[u]["y"]
                x2, y2 = G_proj.nodes[v]["x"], G_proj.nodes[v]["y"]
                return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

            try:
                route_nodes = nx.astar_path(
                    G_proj,
                    origin_node,
                    dest_node,
                    heuristic=heuristic,
                    weight="travel_time",
                )
            except nx.NetworkXNoPath as exc:
                raise HTTPException(
                    status_code=404, detail="No hay ruta posible entre estos puntos"
                ) from exc

            total_dist = 0
            total_time = 0

            for u, v in zip(route_nodes[:-1], route_nodes[1:]):
                edge = G_proj[u][v][0]
                total_dist += edge.get("length", 0)
                total_time += edge.get("travel_time", 0)

            avg_speed_kmh = (total_dist / total_time * 3.6) if total_time > 0 else 0

            turn_instructions = GenerateTourService._generate_turn_by_turn(
                G, route_nodes
            )

            route_coords = []

            first_node = G.nodes[route_nodes[0]]
            route_coords.append((first_node["y"], first_node["x"]))

            for u, v in zip(route_nodes[:-1], route_nodes[1:]):
                edge_data = G[u][v][0]

                if "geometry" in edge_data:

                    detailed_points = [
                        (lat, lon) for lon, lat in edge_data["geometry"].coords
                    ]

                    route_coords.extend(detailed_points[1:])
                else:
                    node_data = G.nodes[v]
                    route_coords.append((node_data["y"], node_data["x"]))

            return GenerateRouteResponse(
                origin=request.origin,
                destination=request.destination,
                total_distance_meters=round(total_dist, 2),
                estimated_duration_seconds=round(total_time, 0),
                average_speed_kmh=round(avg_speed_kmh, 1),
                turn_by_turn_instructions=turn_instructions,
                coords=route_coords,
            )

        except HTTPException:
            raise
        except Exception as exc:
            print(f"ERROR CRÍTICO: {exc}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar ruta: {str(exc)}",
            ) from exc
