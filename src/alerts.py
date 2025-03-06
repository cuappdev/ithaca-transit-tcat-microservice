from datetime import datetime, timezone
import threading
import traceback
import requests


ALERTS_URL = (
    "https://realtimetcatbus.availtec.com/InfoPoint/rest/PublicMessages/GetAllMessages"
)
DATE_STRING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
ONE_MIN_IN_SEC = 60

alerts_data = None


def format_date(date_str):
    # ex) date_str is "/Date(1547528400000-0500)/"
    timestamp = int(date_str[6 : date_str.index("-")]) / 1000.0
    utc_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return utc_date.strftime(DATE_STRING_FORMAT)


def convert_num_to_str(tcat_num):
    num_day_dict = {
        127: "Every day",
        65: "Weekends",
        62: "Weekdays",
        2: "Monday",
        4: "Tuesday",
        8: "Wednesday",
        16: "Thursday",
        32: "Friday",
        64: "Saturday",
        1: "Sunday",
    }
    return num_day_dict.get(tcat_num, "")


def fetch_alerts(event):
    global alerts_data
    try:
        rq = requests.get(ALERTS_URL)
        alerts_data = []
        for alert_dict in rq.json():
            alert = {
                "channelMessages": alert_dict["ChannelMessages"],
                "daysOfWeek": convert_num_to_str(alert_dict["DaysOfWeek"]),
                "fromDate": format_date(alert_dict["FromDate"]),
                "fromTime": format_date(alert_dict["FromTime"]),
                "id": alert_dict["MessageId"],
                "message": alert_dict["Message"],
                "priority": alert_dict["Priority"],
                "routes": alert_dict["Routes"],
                "signs": alert_dict["Signs"],
                "toDate": format_date(alert_dict["ToDate"]),
                "toTime": format_date(alert_dict["ToTime"]),
            }
            alerts_data.append(alert)

    except:
        print(traceback.format_exc())
    threading.Timer(ONE_MIN_IN_SEC, fetch_alerts, [event]).start()


def get_alerts_data():
    return alerts_data
