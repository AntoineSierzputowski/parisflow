import heapq
import json
import os
import unicodedata

_STATIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "stations.json")


def _normalize(name):
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    name = name.lower()
    name = name.replace("'", "").replace("-", " ")
    name = " ".join(name.split())
    return name


def _load_graph():
    with open(_STATIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    stations = {}
    for s in data["stations"]:
        stations[s["name"]] = {
            "x": s["x"],
            "y": s["y"],
            "connections": s["connections"],
        }
    return stations


def _manhattan(s1, s2, stations):
    return abs(stations[s1]["x"] - stations[s2]["x"]) + abs(
        stations[s1]["y"] - stations[s2]["y"]
    )


def _resolve_name(name, stations):
    key = _normalize(name)
    for station_name in stations:
        if _normalize(station_name) == key:
            return station_name
    raise ValueError(
        f"Station '{name}' not found. "
        f"Available: {', '.join(sorted(stations))}"
    )


def dijkstra(start, end):
    """Find the shortest path between two stations using Dijkstra's algorithm.
    Uses Manhattan distance as edge weight.
    Returns the list of station names from start to end.
    """
    stations = _load_graph()
    start = _resolve_name(start, stations)
    end = _resolve_name(end, stations)

    dist = {name: float("inf") for name in stations}
    prev = {name: None for name in stations}
    dist[start] = 0

    # (distance, station_name)
    queue = [(0, start)]

    while queue:
        d, current = heapq.heappop(queue)

        if current == end:
            break

        if d > dist[current]:
            continue

        for neighbor in stations[current]["connections"]:
            weight = _manhattan(current, neighbor, stations)
            new_dist = dist[current] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current
                heapq.heappush(queue, (new_dist, neighbor))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if path[0] != start:
        print(f"No route found between {start} and {end}")
        return []

    print(f"Route from {start} to {end} (distance: {dist[end]}):")
    for i, station in enumerate(path):
        print(f"  {i + 1}. {station}")

    return path
