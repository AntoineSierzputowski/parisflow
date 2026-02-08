import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.stations import get_station_point
from utils.calculat_journey import travel_time_minutes

origin = get_station_point(sys.argv[1])
destination = get_station_point(sys.argv[2])

result = travel_time_minutes(origin, destination)
print(f"{result} minutes")
