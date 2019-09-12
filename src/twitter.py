from calendar import month_abbr
from datetime import datetime
import html
import os

import tweepy


class TwitterAPI:

    DATE_STRING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    NUM_RECENT_STATUSES = 100
    TWITTER_SCREEN_NAME = "IthacaTransit"

    def __init__(self):
        auth = tweepy.OAuthHandler(
            os.environ["TWITTER_KEY"], os.environ["TWITTER_KEY_SECRET"]
        )
        auth.set_access_token(
            os.environ["TWITTER_TOKEN"], os.environ["TWITTER_TOKEN_SECRET"]
        )
        self.api = tweepy.API(auth)

    def convert_str_to_date(self, date_str):
        return datetime.strptime(date_str, self.DATE_STRING_FORMAT)

    def format_alert_status(self, alert):
        """Create a string status from an alert's message and start and end dates."""
        from_date = self.convert_str_to_date(alert["fromDate"])
        to_date = self.convert_str_to_date(alert["toDate"])
        from_date_str = f"{month_abbr[from_date.month]} {from_date.day}"
        if from_date == to_date:
            effective_str = f"Effective: {from_date_str}"
        else:
            to_date_str = f"{month_abbr[to_date.month]} {to_date.day}"
            effective_str = f"Effective: {from_date_str} - {to_date_str}"
        return f"{alert['message']}\n{effective_str}"

    def get_statuses(self, count):
        """Gets the last {count} status objects' extended messages from a twitter
    user's timeline"""
        status_objects = self.api.user_timeline(
            screen_name=self.TWITTER_SCREEN_NAME, count=count, tweet_mode="extended"
        )
        return [
            html.unescape(s.full_text.split("\nEffective: ")[0]) for s in status_objects
        ]

    def get_new_alerts(self, alerts):
        """Filter the array of alerts by removing already tweeted alert messages"""
        statuses = self.get_statuses(self.NUM_RECENT_STATUSES)
        return [a for a in alerts if a["message"] not in statuses]

    def tweet(self, alerts):
        """Makes a request to post tweets with the given alerts"""
        for alert in self.get_new_alerts(alerts):
            status = self.format_alert_status(alert)
            self.api.update_status(status=status)
