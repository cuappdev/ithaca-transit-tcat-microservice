import threading
import time
import os

from flask import Flask, jsonify
from live_tracking import rtf_data, fetch_rtf
from stops import stops_data, fetch_stops

app = Flask(__name__)

@app.route('/live-tracking')
def get_live_tracking():
  return jsonify(rtf_data)

@app.route('/stops')
def get_all_stops():
  return jsonify(stops_data)

if __name__ == '__main__':
  f_stop = threading.Event()
  fetch_rtf(f_stop)
  time.sleep(1)
  app.run(host='0.0.0.0', port=5000)
elif __name__ == 'app':
  f_stop = threading.Event()
  fetch_rtf(f_stop)
