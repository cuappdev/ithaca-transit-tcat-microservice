from datetime import datetime
import threading
import traceback

from auth import fetch_auth_header
import requests

alerts_url = 'https://gateway.api.cloud.wso2.com:443/t/mystop/tcat/v1/rest/PublicMessages/GetAllMessages'
MIN_IN_SEC = 60

alerts_data = None

def convert_to_date(date_str):
  # ex) date_str is "/Date(1547528400000-0500)/"
  timestamp = int(date_str[6:date_str.index('-')]) / 1000.0
  utc_date = datetime.utcfromtimestamp(timestamp)
  return utc_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def convert_num_to_str(tcat_num):
  if tcat_num == 127:
    return 'Every day'
  elif tcat_num == 65:
    return 'Weekends'
  elif tcat_num == 62:
    return 'Weekdays'
  elif tcat_num == 2:
    return 'Monday'
  elif tcat_num == 4:
    return 'Tuesday'
  elif tcat_num == 8:
    return 'Wednesday'
  elif tcat_num == 16:
    return 'Thursday'
  elif tcat_num == 32:
    return 'Friday'
  elif tcat_num == 64:
    return 'Saturday'
  elif tcat_num == 1:
    return 'Sunday'
  return ''

  num_to_str_dict = {
      127: 'Every day',
      65: 'Weekends',
      62: 'Weekdays',
      2: 'Monday',
      4: 'Tuesday',
      8: 'Wednesday',
      16: 'Thursday',
      32: 'Friday',
      64: 'Saturday',
      1: 'Sunday'
  }

def fetch_alerts(stop):
  global alerts_data 
  try:
    auth_header = fetch_auth_header() 
    headers = {
        'Cache-Control': 'no-cache',
        'Authorization': auth_header
    }
    rq = requests.get(alerts_url, headers=headers)
    alerts_data = []
    for alert_dict in rq.json():
      alert = {
          'id': alert_dict.get('MessageId'),
          'message': alert_dict.get('Message'),
          'fromDate': convert_to_date(alert_dict.get('FromDate')),
          'toDate': convert_to_date(alert_dict.get('ToDate')),
          'fromTime': convert_to_date(alert_dict.get('FromTime')),
          'toTime': convert_to_date(alert_dict.get('ToTime')),
          'priority': alert_dict.get('Priority'),
          'daysOfWeek': convert_num_to_str(alert_dict.get('DaysOfWeek')),
          'routes': alert_dict.get('Routes'),
          'signs': alert_dict.get('Signs'),
          'channelMessages': alert_dict.get('ChannelMessages')
      }
      alerts_data.append(alert)
  except:
    print(traceback.format_exc())

  if not stop.is_set():
    threading.Timer(MIN_IN_SEC, fetch_alerts, [stop]).start()

def get_alerts_data():
  return alerts_data
