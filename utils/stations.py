import json
import os
import unicodedata

_STATIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "stations.json")


def _normalize(name):
    """Remove accents, apostrophes, extra spaces and lowercase."""
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    name = name.lower()
    name = name.replace("'", "").replace("-", " ")
    name = " ".join(name.split())
    return name


def _load_stations():
    with open(_STATIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {_normalize(s["name"]): (s["x"], s["y"]) for s in data["stations"]}


_CACHE = None


def get_station_point(station_name):
    """Return (x, y) for a station name.

    The lookup is accent-insensitive, case-insensitive,
    and ignores apostrophes and hyphens.

    Raises ValueError if the station is not found.
    """
    global _CACHE
    if _CACHE is None:
        _CACHE = _load_stations()

    key = _normalize(station_name)
    if key not in _CACHE:
        raise ValueError(
            f"Station '{station_name}' not found. "
            f"Available: {', '.join(sorted(_CACHE))}"
        )
    return _CACHE[key]
