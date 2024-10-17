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
def add_delay(trip,deviceToken):
    global notif_requests
    # notif_requests = fetch_requests()
    if trip in notif_requests:
        notif_requests[trip].append(deviceToken)
    else:
        notif_requests[trip] = [deviceToken]

    save_notifs(notif_requests)
    send_notifs()  
    
#iterates through ths tripIds in the rtf_data to see if any of the delayed
#tripIds have user's waiting to be notified
def send_notifs():
    global notif_requests
    for id in rtf_data:
        if id in notif_requests:
            for user in notif_requests[id]:
                print(user)
                #sends a notification to a device if it is waiting for a delay
                #notification
                send_notif({'deviceToken':user, 'routeID':rtf_data[id]['routeId']})
            #deletes this tripId from notif_requests as it is no longer needed
            print('here')
            del notif_requests[id]
            
    print(notif_requests)
    print('yay')
    save_notifs(notif_requests)
 
def save_notifs(notif_requests):
    with open(json_file_path, "w") as outfile:
        outfile.write(json.dumps(notif_requests))

def start_notif_timer():
    threading.Timer(30, send_notifs).start()

def send_notif(data):
    url = 'http://127.0.0.1:3000/api/v1/microserviceNotif'
    headers = { 'Content-Type': 'application/json' }
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(data)
    print('hi')


def get_rtf_data():
    return rtf_data
