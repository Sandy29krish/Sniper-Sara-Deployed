import requests
from datetime import datetime
import re

NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_expiry_date(symbol):
    try:
        url_map = {
            "BANKNIFTY": "BANKNIFTY",
            "NIFTY": "NIFTY",
            "SENSEX": "SENSEX"
        }
        index = url_map.get(symbol.upper(), symbol.upper())

        response = requests.get(f"https://www.nseindia.com/api/option-chain-indices?symbol={index}", headers=NSE_HEADERS, timeout=10)
        data = response.json()
        expiry_dates = data["records"]["expiryDates"]

        # Return the nearest expiry
        return expiry_dates[0]

    except Exception as e:
        print(f"[NSE Expiry Fetch] Failed for {symbol}: {e}")
        return None

def fetch_nse_option_chain(symbol):
    try:
        url_map = {
            "BANKNIFTY": "BANKNIFTY",
            "NIFTY": "NIFTY",
            "SENSEX": "SENSEX"
        }
        index = url_map.get(symbol.upper(), symbol.upper())
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={index}"

        response = requests.get(url, headers=NSE_HEADERS, timeout=10)
        data = response.json()

        return data["records"]["data"]

    except Exception as e:
        print(f"[NSE Option Chain Fetch] Error for {symbol}: {e}")
        return []

def get_future_price(symbol):
    try:
        url = f"https://www.nseindia.com/api/quote-derivative?symbol={symbol.upper()}"
        response = requests.get(url, headers=NSE_HEADERS, timeout=10)
        data = response.json()
        last_price = float(data["marketDeptOrderBook"]["tradeInfo"]["lastPrice"])
        return last_price
    except Exception as e:
        print(f"[NSE Futures Price] Error for {symbol}: {e}")
        return None
