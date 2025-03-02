import threading
import traceback
import os
import json
import gtfs_realtime_pb2
import urllib.request

import requests

RTF_URL = "https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate"

rtf_data = None
notif_requests = {}

current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, 'notif_requests.json')
f = open(json_file_path)
notif_requests = json.load(f)

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

#adds a deviceToken to a tripID in notifs_request to indicate that this device
#will need to be sent a notification if this tripID is deemed as delayed
def add_delay(trip,stop,deviceToken):
    global notif_requests
    if trip in notif_requests:
        if stop in notif_requests:
            notif_requests[trip][stop].append(deviceToken)
        else:
            notif_requests[trip][stop] = [deviceToken]
    else:
        notif_requests[trip] = {}
        notif_requests[trip][stop] = [deviceToken]

    save_notifs(notif_requests)

def delete_delay(trip,stop,deviceToken):
    global notif_requests
    if trip in notif_requests:
        if stop in notif_requests[trip]:
            notif_requests[trip][stop].remove(deviceToken)
    save_notifs(notif_requests)
     
    
    
#iterates through ths tripIds in the rtf_data to see if any of the delayed
#tripIds have user's waiting to be notified
def send_notifs():
    global notif_requests
    for id in rtf_data:
        if id in notif_requests:
            for stop in notif_requests[id]:
                if stop in rtf_data[id]['stopUpdates']:
                    for user in notif_requests[id][stop]:
                        #sends a notification to a device if it is waiting for a delay
                        #notification
                        send_notif({'deviceToken':user, 'routeID':rtf_data[id]['routeId']})
                    #deletes this tripId from notif_requests as it is no longer needed
                    del notif_requests[id]
            
    save_notifs(notif_requests)
    threading.Timer(30, send_notifs).start()
 
def save_notifs(notif_requests):
    with open(json_file_path, "w") as outfile:
        outfile.write(json.dumps(notif_requests))

def send_notif(data):
    url = 'http://transit-testflight.cornellappdev.com/microserviceNotif'
    headers = { 'Content-Type': 'application/json' }
    response = requests.post(url, json=data, headers=headers)


def get_rtf_data():
    return rtf_data
