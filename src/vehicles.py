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
            congestion_level = entity.vehicle.congestion_level
            current_status = entity.vehicle.current_status
            current_stop_sequence = entity.vehicle.current_stop_sequence
            occupancy_status = entity.vehicle.occupancy_status
            stop_id = entity.vehicle.stop_id
            timestamp = entity.vehicle.timestamp
            if entity.vehicle.HasField("trip"):
                route_id = entity.vehicle.trip.route_id
                trip_id = entity.vehicle.trip.trip_id
            if entity.vehicle.HasField("position"):
                bearing = entity.vehicle.position.bearing
                latitude = entity.vehicle.position.latitude
                longitude = entity.vehicle.position.longitude
                speed = entity.vehicle.position.speed
        entity_dict[vehicle_id] = {
            "bearing": bearing,
            "congestionLevel": congestion_level,
            "currentStatus": current_status,
            "currentStopSequence": current_stop_sequence,
            "latitude": latitude,
            "longitude": longitude,
            "occupancy_status": occupancy_status,
            "routeID": route_id,
            "speed": speed,
            "stopID": stop_id,
            "timestamp": timestamp,
            "tripID": trip_id,
            "vehicleID": vehicle_id,
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
