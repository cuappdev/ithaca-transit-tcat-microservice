import threading
import traceback

from auth import fetch_auth_header
import requests

ONE_HOUR_IN_SEC = 60 * 60
STOPS_URL = 'https://gateway.api.cloud.wso2.com:443/t/mystop/tcat/v1/rest/Stops/GetAllStops'

stops_data = None

def fetch_stops(event):
  global stops_data 
  try:
    auth_header = fetch_auth_header() 
    headers = {
        'Cache-Control': 'no-cache',
        'Authorization': auth_header
    }
    rq = requests.get(STOPS_URL, headers=headers)
    stops_data = [] 
    for stop_dict in rq.json():
      stop = {
          'name': stop_dict.get('Name'),
          'lat': stop_dict.get('Latitude'),
          'long': stop_dict.get('Longitude')
      }
      stops_data.append(stop)
  except:
    print(traceback.format_exc())
  threading.Timer(ONE_HOUR_IN_SEC, fetch_stops, [event]).start()

def get_stops_data():
  return stops_data
