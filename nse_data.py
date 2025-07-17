# nse_data.py

import requests
import datetime

def get_current_expiry():
    """
    Gets the nearest Thursday expiry from today.
    If today is Thursday before 3:30 PM, returns today.
    If it's Friday or expiry has passed, gives next Thursday.
    """
    today = datetime.date.today()
    weekday = today.weekday()

    if weekday == 3 and datetime.datetime.now().time() < datetime.time(15, 30):
        return today.strftime('%d-%b-%Y').upper()
    
    days_ahead = 3 - weekday if weekday <= 3 else 10 - weekday
    next_expiry = today + datetime.timedelta(days=days_ahead)
    return next_expiry.strftime('%d-%b-%Y').upper()

def get_futures_price(symbol):
    """
    Fetch current futures LTP from NSE India
    """
    url = f"https://www.nseindia.com/api/quote-derivative?symbol={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        for item in data['stocks']:
            if item['metadata']['instrumentType'] == 'FUTIDX':
                return float(item['metadata']['lastPrice'])
        return None
    except:
        print(f"[NSE] Failed to fetch futures price for {symbol}")
        return None

def get_option_chain(symbol):
    """
    Get full option chain from NSE
    """
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()['records']['data']
        option_chain = []

        for item in data:
            strike = item.get('strikePrice')
            ce = item.get('CE')
            pe = item.get('PE')

            if ce:
                option_chain.append({
                    "strike": ce['strikePrice'],
                    "type": "CE",
                    "last_price": ce['lastPrice']
                })
            if pe:
                option_chain.append({
                    "strike": pe['strikePrice'],
                    "type": "PE",
                    "last_price": pe['lastPrice']
                })

        return option_chain
    except:
        print(f"[NSE] Failed to fetch option chain for {symbol}")
        return []

def is_nse_live():
    """
    Ping NSE homepage to check if it's live
    """
    try:
        response = requests.get("https://www.nseindia.com", timeout=5)
        return response.status_code == 200
    except:
        return False
