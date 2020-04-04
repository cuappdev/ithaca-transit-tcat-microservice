import threading
import traceback

import gtfs_realtime_pb2
import urllib.request

VEHICLES_URL = "https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=VehiclePosition&serverid=0"

vehicles_data = None


def parse_protobuf(rq):
    entity_dict = {}
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(rq.read())
    for entity in feed.entity:
        vehicle_id = entity.id
        if entity.HasField("vehicle"):
            timestamp = entity.vehicle.timestamp
            congestion_level = entity.vehicle.congestion_level
            if entity.vehicle.HasField("trip"):
                trip_id = entity.vehicle.trip.trip_id
                route_id = entity.vehicle.trip.route_id
            if entity.vehicle.HasField("position"):
                longitude = entity.vehicle.position.longitude
                latitude = entity.vehicle.position.latitude
                bearing = entity.vehicle.position.bearing
                speed = entity.vehicle.position.speed
        entity_dict[vehicle_id] = {
            "bearing": bearing,
            "congestion_level": congestion_level,
            "latitude": latitude,
            "longitude": longitude,
            "routeID": route_id,
            "speed": speed,
            "timestamp": timestamp,
            "tripID": trip_id,
        }
    return entity_dict


def fetch_vehicles(event):
    global vehicles_data
    try:
        rq = urllib.request.urlopen(VEHICLES_URL)
        vehicles_data = parse_protobuf(rq)
    except:
        print(traceback.format_exc())
    threading.Timer(30, fetch_vehicles, [event]).start()


def get_vehicles_data():
    return vehicles_data
