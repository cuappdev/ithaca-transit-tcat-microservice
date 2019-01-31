import threading
import traceback
import os

from auth import fetch_auth_header
import requests
import xmltodict

HOUR_IN_SEC = 60 * 60
stops_url = 'https://gateway.api.cloud.wso2.com:443/t/mystop/tcat/v1/rest/Stops/GetAllStops'

stops_data = None

def fetch_stops(stop):
    global stops_data 
    try:
      auth_header = fetch_auth_header() 
      headers = {
          'Cache-Control': 'no-cache',
          'Authorization': auth_header
      }
      rq = requests.get(stops_url, headers=headers)
      stops_data = [] 
      for stop in rq.json():
        stop = {
            'name': stop.get('Name'),
            'lat': stop.get('Latitude'),
            'long': stop.get('Longitude')
        }
        stops_data.append(stop)
    except:
      print(traceback.format_exc())

    if not stop.is_set():
      threading.Timer(HOUR_IN_SEC, fetch_stops, [stop]).start()

