import os
import threading
import traceback

import requests
import xmltodict

RTF_URL = 'https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate&debug=true'

rtf_data = None

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

def fetch_rtf(event):
  global rtf_data
  try:
    rq = requests.get(RTF_URL, headers={'Cache-Control': 'no-cache'}, timeout=3)
    rtf_data = parse_xml_to_json(rq.text)
  except:
    print(traceback.format_exc())
  threading.Timer(30, fetch_rtf, [event]).start()

def get_rtf_data():
  return rtf_data
