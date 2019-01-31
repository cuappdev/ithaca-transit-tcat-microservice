import threading
import time
import os

from alerts import get_alerts_data, fetch_alerts
from flask import Flask, jsonify
from live_tracking import rtf_data, fetch_rtf
from stops import stops_data, fetch_stops

app = Flask(__name__)

@app.route('/alerts')
def get_alerts():
  alerts_data = get_alerts_data()
  if alerts_data is None:
    return jsonify({'success': False, 'errors': ['Failed to get alerts']})
  return jsonify({'success': True, 'data': alerts_data})

@app.route('/live-tracking')
def get_live_tracking():
  return jsonify(rtf_data)

@app.route('/stops')
def get_all_stops():
  return jsonify(stops_data)

if __name__ == '__main__':
  f_stop = threading.Event()
  fetch_rtf(f_stop)
  fetch_stops(f_stop)
  fetch_alerts(f_stop)
  time.sleep(1)
  app.run(host='0.0.0.0', port=5000)
elif __name__ == 'app':
  f_stop = threading.Event()
  fetch_rtf(f_stop)
