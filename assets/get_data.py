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
    list_markets = [
        {
            'label': df.name[i],
            'value': df.symbol[i]
        }
        for i in df.loc[df.active].index  # We just want to display the markets that are active
    ]
    return list_markets


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
    list_pairs = [
        {
            'label': df.pair[i].upper(),
            'value': df.pair[i]
        }
        for i in df.loc[df.active].index  # We just want to display the pairs that are active on the given market
    ]
    return list_pairs


# get data for OHLC chart
def ohlc(market, pair, before=None, after=None, periods=None):
    url = fr"https://api.cryptowat.ch/markets/{market}/{pair}/ohlc"
    params = {
        "apikey": api_key,
        "before": before,  # Unix timestamp. Only return candles opening before this time. Example: 1481663244
        "after": after,  # Unix timestamp. Only return candles opening after this time. Example 1481663244
        "periods": periods  # comma separated integers. Only return these time periods.
    }
    result = requests.get(url, params=params).json()
    if "result" not in result.keys():
        return pd.DataFrame()
    list_ = []
    values = [60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200, 604800]
    labels = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d", "3d", "1w"]
    new_keys = []
    for key in result["result"].keys():
        try:
            new_keys.append(int(key))
        except:
            pass
    for key in new_keys:
        df = pd.DataFrame(result["result"][str(key)],
                          columns=["CloseTime", "OpenPrice", "HighPrice", "LowPrice", "ClosePrice", "Volume",
                                   "QuoteVolume"])
        df["Period"] = [key for _ in df.index]
        ii = values.index(key)
        df["Label"] = [labels[ii] for _ in df.index]
        list_.append(df)
    final_df = pd.concat(list_)
    final_df = final_df.sort_values(["Period", "CloseTime"])
    return final_df
