from collections import defaultdict
import math
import threading
import traceback

from src.auth import fetch_auth_header
import geopy.distance
import requests

BUS_STOP = "busStop"
COLLEGETOWN_STOP = {  # Creating "fake" bus stop to remove Google Places central Collegetown location choice
    "name": "Collegetown",
    "lat": 42.442558,
    "long": -76.485336,
    "type": BUS_STOP,
}
MIN_DIST_BETWEEN_STOPS = 160.0  # Measured in meters
ONE_HOUR_IN_SEC = 60 * 60
STOPS_URL = "https://realtimetcatbus.availtec.com/InfoPoint/rest/Stops/GetAllStops"

stops_data = None


def fetch_stops(event):
    global stops_data
    try:
        rq = requests.get(STOPS_URL)
        stops = []
        for stop_dict in rq.json():
            stop = {
                "name": stop_dict.get("Name"),
                "lat": stop_dict.get("Latitude"),
                "long": stop_dict.get("Longitude"),
                "type": BUS_STOP,
            }
            stops.append(stop)
        stops.append(COLLEGETOWN_STOP)
        stops_data = filter_stops(stops)
    except:
        print(traceback.format_exc())
    threading.Timer(ONE_HOUR_IN_SEC, fetch_stops, [event]).start()


def filter_stops(stops):
    # Create dictionary of stop names to stop information
    stop_names_to_info = defaultdict(list)
    for stop in stops:
        stop_names_to_info[stop["name"]].append(stop)

    # Get all stops with and without duplicate names
    non_duplicate_stops = [stops_info[0] for stops_info in stop_names_to_info.values() if len(stops_info) == 1]
    duplicate_stops = [stops_info for stops_info in stop_names_to_info.values() if len(stops_info) > 1]

    # Go through the stops with duplicate names
    for bus_stops in duplicate_stops:
        first_stop = bus_stops[0]
        last_stop = bus_stops[-1]
        first_coords = (first_stop["lat"], first_stop["long"])
        last_coords = (last_stop["lat"], last_stop["long"])

        distance = geopy.distance.distance(first_coords, last_coords).m
        # If stops are too close to each other, combine into a new stop with averaged location
        if distance < MIN_DIST_BETWEEN_STOPS:
            middle_lat, middle_long = get_middle_coordinate(first_coords, last_coords)
            middle_stop = {"name": first_stop["name"], "lat": middle_lat, "long": middle_long, "type": BUS_STOP}
            non_duplicate_stops.append(middle_stop)
        else:  # Otherwise, add directly to list of stops
            non_duplicate_stops.append(first_stop)
            non_duplicate_stops.append(last_stop)

    # Lastly, sort by alphabetical order
    sorted_stops = sorted(non_duplicate_stops, key=lambda k: k["name"].upper())
    return sorted_stops


def get_middle_coordinate(coord_a, coord_b):
    # Get the coordinate in the middle of coord_a and coord_b
    a_lat = math.radians(coord_a[0])
    a_long = math.radians(coord_a[1])
    b_lat = math.radians(coord_b[0])
    b_long = math.radians(coord_b[1])
    long_diff = b_long - a_long
    x = math.cos(b_lat) * math.cos(long_diff)
    y = math.cos(b_lat) * math.sin(long_diff)

    middle_lat = math.atan2(math.sin(a_lat) + math.sin(b_lat), math.sqrt((math.cos(a_lat) + x) ** 2 + y ** 2))
    middle_long = a_long + math.atan2(y, math.cos(a_lat) + x)

    return math.degrees(middle_lat), math.degrees(middle_long)


def get_stops_data():
    return stops_data
