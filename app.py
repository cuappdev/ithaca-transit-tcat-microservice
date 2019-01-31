import threading
import time
import traceback
import os

from flask import Flask, jsonify
import requests
import xmltodict

app = Flask(__name__)
URL = 'https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate&debug=true'

data = None

def parse_xml_to_json(xml):
    ret = xmltodict.parse(xml).popitem()[1]

    entities = ret['Entities'].popitem()[1]
    entity_dict = {}

    timestamp = ret['Header']['Timestamp']
    entity_dict['Timestamp'] = timestamp

    for entity in entities:
        entity_id = entity['Id']
        trip_update = entity['TripUpdate']

        vehicle_id = None
        if 'Vehicle' in trip_update:
            vehicle_id = trip_update['Vehicle']['Id']

        route_id = trip_update['Trip']['RouteId']
        delay = trip_update['Delay']

        stop_updates = {}
        for k in trip_update['StopTimeUpdates']:
            stop_time_updates = trip_update['StopTimeUpdates'][k]

            if isinstance(stop_time_updates, type([])):
                for stop_update in stop_time_updates:
                    stop_id = stop_update['StopId']
                    stop_updates[stop_id] = stop_update['Arrival']['Delay']
            else:
                stop_id = stop_time_updates['StopId']
                stop_updates[stop_id] = stop_time_updates['Arrival']['Delay']

        entity_dict[entity_id] = {
            'delay': delay,
            'routeId': route_id,
            'stopUpdates': stop_updates,
            'vehicleId': vehicle_id
        }
    return entity_dict

def f(stop):
    global data
    try:
        rq = requests.get(URL, headers={'Cache-Control': 'no-cache'})
        data = parse_xml_to_json(rq.text)
    except:
        print(traceback.format_exc())

    if not f_stop.is_set():
        threading.Timer(1, f, [stop]).start()

@app.route('/')
def get_live_tracking():
    return jsonify(data)

if __name__ == '__main__':
    f_stop = threading.Event()
    f(f_stop)
    time.sleep(1)
    app.run(host='0.0.0.0', port=5000)
elif __name__ == 'app':
    f_stop = threading.Event()
    f(f_stop)
