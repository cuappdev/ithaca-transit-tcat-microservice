from datetime import datetime
import threading
import traceback

import requests

from auth import fetch_auth_header

ALERTS_URL = 'https://gateway.api.cloud.wso2.com:443/t/mystop/tcat/v1/rest/PublicMessages/GetAllMessages'
ONE_MIN_IN_SEC = 60

alerts_data = None

def convert_to_date(date_str):
  # ex) date_str is "/Date(1547528400000-0500)/"
  timestamp = int(date_str[6:date_str.index('-')]) / 1000.0
  utc_date = datetime.utcfromtimestamp(timestamp)
  return utc_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def convert_num_to_str(tcat_num):
  num_day_dict = {
      127: 'Every day',
      65: 'Weekends',
      62: 'Weekdays',
      2: 'Monday',
      4: 'Tuesday',
      8: 'Wednesday',
      16: 'Thursday',
      32: 'Friday',
      64: 'Saturday',
      1: 'Sunday',
  }
  return num_day_dict.get(tcat_num, '')

def fetch_alerts(event):
  global alerts_data 
  try:
    auth_header = fetch_auth_header() 
    headers = {
        'Authorization': auth_header,
        'Cache-Control': 'no-cache'
    }
    rq = requests.get(ALERTS_URL, headers=headers)
    alerts_data = []
    for alert_dict in rq.json():
      alert = {
          'channelMessages': alert_dict.get('ChannelMessages'),
          'daysOfWeek': convert_num_to_str(alert_dict.get('DaysOfWeek')),
          'fromDate': convert_to_date(alert_dict.get('FromDate')),
          'fromTime': convert_to_date(alert_dict.get('FromTime')),
          'id': alert_dict.get('MessageId'),
          'message': alert_dict.get('Message'),
          'priority': alert_dict.get('Priority'),
          'routes': alert_dict.get('Routes'),
          'signs': alert_dict.get('Signs'),
          'toDate': convert_to_date(alert_dict.get('ToDate')),
          'toTime': convert_to_date(alert_dict.get('ToTime'))
      }
      alerts_data.append(alert)
  except:
    print(traceback.format_exc())
  threading.Timer(ONE_MIN_IN_SEC, fetch_alerts, [event]).start()

def get_alerts_data():
  return alerts_data
