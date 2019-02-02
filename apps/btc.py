from urllib.request import urlopen, Request
from urllib.error import HTTPError
from json import load


def get_btc_value(res):
    try:
        return "Current value of Bitcoin in USD: ${:0.2f}".format(res['bpi']['USD']['rate_float'])
    except KeyError:
        return "Don't panic, but the API is returning an invalid format. Verify JSON response."


def btc_value():
    try:
        req = Request("https://api.coindesk.com/v1/bpi/currentprice.json",
                      headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as f:
            return get_btc_value(load(f))
    except HTTPError:
        return "Server Error."
