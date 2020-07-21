# local imports
from assets.conf import api_key

# imports
import requests
import pandas as pd


# get a list of markets available from cryptowat.ch
# This will be used on the dropdown menu
# The function will return a list of dicts


def market_list():
    url = r"https://api.cryptowat.ch/exchanges"
    params = {
        "apikey": api_key
    }
    result = requests.get(url, params=params).json()
    df = pd.DataFrame(result["result"]).sort_values("name")
    final = [
        {
            'label': df.name[i],
            'value': df.symbol[i]
        }
        for i in df.loc[df.active].index  # We just want to display the markets that are active
    ]
    return final


# get a list of pairs for the selected market
# This will be used on the dropdown menu
# The function will return a list of dicts


def pairs_list(market):
    url = fr"https://api.cryptowat.ch/markets/{market}"
    params = {
        "apikey": api_key
    }
    result = requests.get(url, params=params).json()
    df = pd.DataFrame(result["result"]).sort_values("pair")
    final = [
        {
            'label': df.pair[i].upper(),
            'value': df.pair[i]
        }
        for i in df.loc[df.active].index  # We just want to display the pairs that are active on the given market
    ]
    return final
