from datetime import datetime, timedelta
import os
import requests
import traceback

TOKEN_URL = "https://gateway.api.cloud.wso2.com:443/token"

access_token = None
expiration_date = None


def is_access_token_expired():
    # First time fetching token
    if access_token is None or expiration_date is None:
        return True
    # 1 second expiration buffer
    earlier_exp_date = expiration_date + timedelta(0, -1)
    return datetime.now() > earlier_exp_date


def fetch_access_token():
    basic_token = os.environ["TOKEN"]
    headers = {"Cache-Control": "no-cache", "Authorization": "Basic {}".format(basic_token)}
    global access_token, expiration_date
    try:
        rq = requests.post(TOKEN_URL, headers=headers, data={"grant_type": "client_credentials"})
        print('here!')
        res = rq.json()
        print(rq.content)
        print(res.get("expires_in"))
        access_token = res.get("access_token")
        expires_in = res.get("expires_in")
        expiration_date = datetime.now() + timedelta(0, expires_in)
    except:
        print('here!')
        print(requests.post(TOKEN_URL, headers=headers, data={"grant_type": "client_credentials"}).headers.get('content-type'))
        print(traceback.format_exc())


def fetch_auth_header():
    if is_access_token_expired():
        fetch_access_token()
    return "Bearer {}".format(access_token)
