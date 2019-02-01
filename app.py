import threading
import time
import os

from flask import Flask, jsonify

from alerts import get_alerts_data, fetch_alerts
from live_tracking import get_rtf_data, fetch_rtf
from stops import get_stops_data, fetch_stops

app = Flask(__name__)

@app.route('/alerts')
def get_alerts():
  return jsonify(get_alerts_data())

@app.route('/')
@app.route('/rtf')
def get_rtf():
  return jsonify(get_rtf_data())

@app.route('/stops')
def get_all_stops():
  return jsonify(get_stops_data())

if __name__ == '__main__':
  rtf_event, stops_event, alerts_event = [threading.Event() for i in range(3)]
  fetch_rtf(rtf_event)
  fetch_stops(stops_event)
  fetch_alerts(alerts_event)
  time.sleep(1)
  app.run(host='0.0.0.0', port=5000)
elif __name__ == 'app':
  rtf_event, stops_event, alerts_event = [threading.Event() for i in range(3)]
  fetch_rtf(rtf_event)
  fetch_stops(stops_event)
  fetch_alerts(alerts_event)

