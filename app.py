import threading
import os

from flask import Flask
import requests

app = Flask(__name__)
URL = 'https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=TripUpdate&debug=true'

data = requests.get(URL, headers={'Cache-Control': 'no-cache'}).text

def f(f_stop):
    global data
    rq = requests.get(URL, headers={'Cache-Control': 'no-cache'})
    data = rq.text
    if not f_stop.is_set():
        threading.Timer(1, f, [f_stop]).start()

@app.route('/')
def get_live_tracking():
    return data

if __name__ == '__main__':
    f_stop = threading.Event()
    f(f_stop)
    app.run(host='0.0.0.0', port=5000)
