import threading
import time
import json
from flask import Flask, jsonify, request

from src.alerts import fetch_alerts, get_alerts_data
from src.gtfs import fetch_gtfs, get_gtfs_data, get_gtfs_feed_info
from src.live_tracking import fetch_rtf, get_rtf_data, add_delay,start_notif_timer
from src.stops import fetch_stops, get_stops_data
from src.vehicles import fetch_vehicles, get_vehicles_data

app = Flask(__name__)



@app.route("/alerts")
def get_alerts():
    return jsonify(get_alerts_data())


@app.route("/gtfs")
def get_gtfs():
    return jsonify(get_gtfs_data())


@app.route("/")
@app.route("/rtf")
def get_rtf():
    print('bye2')
    return jsonify(get_rtf_data())


@app.route("/stops")
def get_all_stops():
    return jsonify(get_stops_data())


@app.route("/gtfs-feed-info")
def get_gtfs_date():
    return jsonify(get_gtfs_feed_info())


@app.route("/vehicles")
def get_vehicles():
    return jsonify(get_vehicles_data())

@app.route("/delayNotifs/", methods=["POST"])
def get_delayNotifs():
    #notif_requests = {'t65B-b1F42-slC':'hi'}
    body = json.loads(request.data)
    trip = body.get("tripId")
    print(body)
    deviceToken = body.get("deviceToken")

    add_delay(trip,deviceToken)
    return jsonify({"success":True})
  



if __name__ == "__main__":
    alerts_event, gtfs_event, rtf_event, stops_event, vehicles_event = [threading.Event() for i in range(5)]
    fetch_alerts(alerts_event)
    fetch_gtfs(gtfs_event)
    fetch_rtf(rtf_event)
    fetch_stops(stops_event)
    fetch_vehicles(vehicles_event)
    start_notif_timer()
    time.sleep(1)
    app.run(host="0.0.0.0", port=8000)
elif __name__ == "app":
    alerts_event, gtfs_event, rtf_event, stops_event, vehicles_event = [threading.Event() for i in range(5)]
    fetch_alerts(alerts_event)
    fetch_gtfs(gtfs_event)
    fetch_rtf(rtf_event)
    fetch_stops(stops_event)
    fetch_vehicles(vehicles_event)
    start_notif_timer()
