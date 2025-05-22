from collections import defaultdict

from .dijkstra import dijkstra, reconstruct_path
from .utils import *
from database.subway import *


def build_subway_graph(con):
    subway_connections = get_subway_connections(con)

    graph = defaultdict(list)
    for origin, destination, duration in subway_connections:
        graph[origin].append((destination, duration))
        graph[destination].append((origin, duration))

    return graph


def find_shoref_subway_path(con, start, end, stations):
    start_id = get_station_id_by_name(start, stations)
    end_id = get_station_id_by_name(end, stations)

    graph = build_subway_graph(con)
    distances, previous = dijkstra(graph, start_id)
    path = reconstruct_path(previous, end_id)

    return path, distances[end_id]


def segment_path_by_line(path, stations):
    segments, current_line, via = [], None, []

    for i in range(1, len(path)):
        prev, curr = path[i - 1], path[i]
        line = infer_line(prev, curr, current_line, stations)
        via.append(prev)

        if line != current_line:
            if current_line is not None:
                segments[-1]["to"] = prev
                segments[-1]["via"] = via

                via = [prev] if line in stations[prev]["lines"] else []

            if line in stations[prev]["lines"]:
                segments.append({"line": line, "from": prev})
            else:
                segments.append({"line": line, "from": curr})

            current_line = line

    via.append(curr)

    segments[-1]["to"] = path[-1]
    segments[-1]["via"] = via
    return segments


def build_route_steps(segments, stations, lines):
    steps = []
    for i, segment in enumerate(segments):
        from_station = stations[segment["from"]]
        to_station = stations[segment["to"]]
        line = segment["line"]
        direction = get_direction(
            from_station["id"], to_station["id"], line, stations, lines
        )

        via = []
        for station_id in segment["via"]:
            station = stations[station_id]
            via.append({"id": station["id"], "name": station["name"]})

        steps.append(
            {
                "type": "embark",
                "line": line,
                "direction": direction,
                "from_station": {
                    "id": from_station["id"],
                    "name": from_station["name"],
                },
                "to_station": {"id": to_station["id"], "name": to_station["name"]},
                "via": via,
            }
        )

        if i < len(segments) - 1:
            next_line = segments[i + 1]["line"]
            steps.append(
                {
                    "type": "transfer",
                    "at": {"id": to_station["id"], "name": to_station["name"]},
                    "from_line": line,
                    "to_line": next_line,
                }
            )

    return steps


def find_subway_route(con, origin, destination):
    stations = get_stations(con)
    lines = get_lines(con)

    path, trip_duration = find_shoref_subway_path(con, origin, destination, stations)

    segments = segment_path_by_line(path, stations)
    steps = build_route_steps(segments, stations, lines)

    return {"steps": steps, "estimated_duration": trip_duration}
