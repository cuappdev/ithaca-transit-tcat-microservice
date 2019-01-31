import threading
import traceback
import os

import requests
import xmltodict

rtf_url = 'https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate&debug=true'

rtf_data = None

def parse_xml_to_json(xml):
    namespaces = {'Header': None}
    ret = xmltodict.parse(xml, process_namespaces=True, namespaces=namespaces).popitem()

    entities = ret[1].popitem()[1].popitem()
    entity_dict = {}

    timestamp = ret[1]['Header']['Timestamp']
    entity_dict['Timestamp'] = timestamp

    for entity in entities[1]:
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
                    departure_delay = stop_update['Departure']['Delay']
                    stop_updates[stop_id] = departure_delay
            else:
                stop_id = stop_time_updates['StopId']
                departure_delay = stop_time_updates['Departure']['Delay']
                stop_updates[stop_id] = departure_delay

        entity_dict[entity_id] = {
            'delay': delay,
            'routeId': route_id,
            'stopUpdates': stop_updates,
            'vehicleId': vehicle_id
        }
    return entity_dict

def fetch_rtf(stop):
    global rtf_data
    try:
        rq = requests.get(rtf_url, headers={'Cache-Control': 'no-cache'})
        rtf_data = parse_xml_to_json(rq.text)
    except:
        print(traceback.format_exc())

    if not stop.is_set():
      threading.Timer(1, fetch_rtf, [stop]).start()
