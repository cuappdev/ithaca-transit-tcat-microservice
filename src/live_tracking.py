import threading
import traceback

import json
import requests

RTF_URL = "https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate&debug=true"

rtf_data = None


def parse_json(json_rtf):
    ret = json.loads(json_rtf)

    entities = ret["Entities"]

    entity_dict = {}

    timestamp = ret["Header"]["Timestamp"]
    entity_dict["Timestamp"] = timestamp

    for entity in entities:
        entity_id = entity["Id"]
        trip_update = entity["TripUpdate"]

        vehicle_id = None
        if trip_update.get("Vehicle"):
            vehicle_id = trip_update["Vehicle"]["Id"]

        route_id = trip_update["Trip"]["RouteId"]

        stop_updates = {}

        for stop_time_updates in trip_update["StopTimeUpdates"]:
            if isinstance(stop_time_updates, type([])):
                for stop_update in stop_time_updates:
                    if stop_update["schedule_relationship"] == "NoData":
                        continue
                    stop_id = stop_update["StopId"]
                    stop_updates[stop_id] = stop_update["Arrival"]["Delay"]
            elif stop_time_updates["schedule_relationship"] != "NoData" and stop_time_updates["Arrival"]:
                stop_id = stop_time_updates["StopId"]
                stop_updates[stop_id] = stop_time_updates["Arrival"]["Delay"]

        entity_dict[entity_id] = {"routeId": route_id, "stopUpdates": stop_updates, "vehicleId": vehicle_id}
    return entity_dict


def fetch_rtf(event):
    global rtf_data
    try:
        rq = requests.get(RTF_URL, headers={"Cache-Control": "no-cache"}, timeout=3)
        rtf_data = parse_json(rq.text)
    except:
        print(traceback.format_exc())
    threading.Timer(30, fetch_rtf, [event]).start()


def get_rtf_data():
    return rtf_data
