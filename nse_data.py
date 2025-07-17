# nse_data.py

import requests
from datetime import datetime
import json

NSE_OPTION_CHAIN_URL = "https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

def get_nse_session():
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=NSE_HEADERS)
    return session

def get_option_chain(symbol="NIFTY"):
    try:
        session = get_nse_session()
        url = NSE_OPTION_CHAIN_URL.format(symbol=symbol.upper())
        response = session.get(url, headers=NSE_HEADERS)
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ Error fetching option chain: {e}")
        return None

def get_expiry_dates(symbol="NIFTY"):
    data = get_option_chain(symbol)
    if data:
        return data['records']['expiryDates']
    return []

def get_spot_price(symbol="NIFTY"):
    data = get_option_chain(symbol)
    if data:
        return float(data['records']['underlyingValue'])
    return None

def get_option_chain_data(symbol="NIFTY", expiry=None):
    data = get_option_chain(symbol)
    if not data:
        return []

    all_data = data['records']['data']
    filtered = []
    for entry in all_data:
        if entry.get("expiryDate") == expiry:
            if "CE" in entry and "PE" in entry:
                ce = entry["CE"]
                pe = entry["PE"]
                filtered.append({
                    "strike": ce["strikePrice"],
                    "CE": {
                        "strike": ce["strikePrice"],
                        "last_price": ce.get("lastPrice", 0),
                        "open_interest": ce.get("openInterest", 0),
                        "change_oi": ce.get("changeinOpenInterest", 0)
                    },
                    "PE": {
                        "strike": pe["strikePrice"],
                        "last_price": pe.get("lastPrice", 0),
                        "open_interest": pe.get("openInterest", 0),
                        "change_oi": pe.get("changeinOpenInterest", 0)
                    }
                })
    return filtered
