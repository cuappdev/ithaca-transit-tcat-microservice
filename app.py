import threading
import time
import os

from flask import Flask, jsonify

from src.alerts import get_alerts_data, fetch_alerts
from src.gtfs import get_gtfs_data, fetch_gtfs
from src.live_tracking import get_rtf_data, fetch_rtf
from src.stops import get_stops_data, fetch_stops

app = Flask(__name__)

@app.route('/alerts')
def get_alerts():
  return jsonify(get_alerts_data())

@app.route('/gtfs')
def get_gtfs():
  return jsonify(get_gtfs_data())

@app.route('/')
@app.route('/rtf')
def get_rtf():
  return jsonify(get_rtf_data())

@app.route('/stops')
def get_all_stops():
  return jsonify(get_stops_data())

if __name__ == '__main__':
  alerts_event, gtfs_event, rtf_event, stops_event = [threading.Event() for i in range(4)]
  fetch_alerts(alerts_event)
  fetch_gtfs(gtfs_event)
  fetch_rtf(rtf_event)
  fetch_stops(stops_event)
  time.sleep(1)
  app.run(host='0.0.0.0', port=5000)
elif __name__ == 'app':
  alerts_event, gtfs_event, rtf_event, stops_event = [threading.Event() for i in range(4)]
  fetch_alerts(alerts_event)
  fetch_gtfs(gtfs_event)
  fetch_rtf(rtf_event)
  fetch_stops(stops_event)
