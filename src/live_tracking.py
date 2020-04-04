import threading
import traceback

import gtfs_realtime_pb2
import urllib.request

RTF_URL = "https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate"

rtf_data = None


def parse_protobuf(rq):
    entity_dict = {}
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(rq.read())
    vehicle_id = None
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            if entity.trip_update.HasField("vehicle"):
                vehicle_id = entity.trip_update.vehicle.id
            route_id = entity.trip_update.trip.route_id
            stop_updates = {}
            for stop_update in entity.trip_update.stop_time_update:
                if stop_update.schedule_relationship == "NoData":
                    continue
                stop_id = stop_update.stop_id
                stop_updates[stop_id] = stop_update.arrival.delay
        entity_dict[entity.id] = {"routeId": route_id, "stopUpdates": stop_updates, "vehicleId": vehicle_id}
    return entity_dict


def fetch_rtf(event):
    global rtf_data
    try:
        rq = urllib.request.urlopen(RTF_URL)
        rtf_data = parse_protobuf(rq)
    except:
        print(traceback.format_exc())
    threading.Timer(30, fetch_rtf, [event]).start()


def get_rtf_data():
    return rtf_data
