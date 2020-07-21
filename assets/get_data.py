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
