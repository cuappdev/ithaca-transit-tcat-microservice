from datetime import datetime
import gtfs_realtime_pb2
import threading
import traceback
import urllib.request

from src.twitter import TwitterAPI

ALERTS_URL = "https://realtimetcatbus.availtec.com/InfoPoint/GTFS-Realtime.ashx?&Type=Alert"
DATE_STRING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
ONE_MIN_IN_SEC = 60

alerts_data = None
twitter_api = TwitterAPI()


def format_date(epoch):
    d = datetime.fromtimestamp(epoch)
    return d.strftime(DATE_STRING_FORMAT)


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


def get_alert_text(entity):
    # translation is a list, but usually only has one element
    text = [t.text for t in entity.alert.description_text.translation]
    return " ".join(text)


def get_dates(entity):
    # active_period is a list, but most likely will only have one element
    if len(entity.alert.active_period) > 0:
        from_date = entity.alert.active_period[0].start
        to_date = entity.alert.active_period[0].end
        return {"from_date": format_date(from_date), "to_date": format_date(to_date)}


def fetch_alerts(event):
    global alerts_data
    try:
        rq = urllib.request.urlopen(ALERTS_URL)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(rq.read())
        alerts_data = []
        # for alert_dict in rq.json():
        #     alert = {
        #         "channelMessages": alert_dict["ChannelMessages"],
        #         "daysOfWeek": convert_num_to_str(alert_dict["DaysOfWeek"]),
        #         "fromDate": format_date(alert_dict["FromDate"]),
        #         "fromTime": format_date(alert_dict["FromTime"]),
        #         "id": alert_dict["MessageId"],
        #         "message": alert_dict["Message"],
        #         "priority": alert_dict["Priority"],
        #         "routes": alert_dict["Routes"],
        #         "signs": alert_dict["Signs"],
        #         "toDate": format_date(alert_dict["ToDate"]),
        #         "toTime": format_date(alert_dict["ToTime"]),
        #     }
        #     alerts_data.append(alert)
        for entity in feed.entity:
            dates = get_dates(entity)
            alert = {
                "channelMessages": [],
                "fromDate": dates["from_date"],
                "toDate": dates["to_date"],
                "message": get_alert_text(entity),
                "id": entity.id,
            }
            print(alert)
            alerts_data.append(alert)
        # twitter_api.tweet(alerts_data)
    except:
        print(traceback.format_exc())
    threading.Timer(ONE_MIN_IN_SEC, fetch_alerts, [event]).start()


def get_alerts_data():
    return alerts_data
