def manhattan_distance(point_a, point_b):
    """Calculate Manhattan distance in km"""
    x1, y1 = point_a
    x2, y2 = point_b
    return abs(x2 - x1) + abs(y2 - y1)

def travel_time_minutes(point_a, point_b, speed_kmh=40):
    """Calculate travel time in minutes at constant speed"""
    distance_km = manhattan_distance(point_a, point_b)
    return (distance_km / speed_kmh) * 60