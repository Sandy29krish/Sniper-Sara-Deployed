nse_data.py

import requests from datetime import datetime import pytz

NSE_BASE_URL = "https://www.nseindia.com/api" HEADERS = { "User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9", }

def get_index_futures_price(symbol): """ Fetch live futures price of given index (NIFTY, BANKNIFTY, SENSEX) """ try: url = f"https://www.nseindia.com/api/quote-derivative?symbol={symbol.upper()}" response = requests.get(url, headers=HEADERS, timeout=10) data = response.json() for item in data.get("stocks", []): if item.get("metadata", {}).get("instrumentType") == "FUTIDX": return float(item["metadata"]["lastPrice"]) return None except Exception as e: print(f"[NSE DATA] Error fetching futures price for {symbol}: {e}") return None

def get_expiry_date(symbol): """ Get next expiry date for index """ try: url = f"{NSE_BASE_URL}/option-chain-indices?symbol={symbol.upper()}" response = requests.get(url, headers=HEADERS, timeout=10) data = response.json() expiry_dates = data.get("records", {}).get("expiryDates", []) if expiry_dates: tz = pytz.timezone("Asia/Kolkata") dt = datetime.strptime(expiry_dates[0], "%d-%b-%Y").astimezone(tz) return dt.strftime("%Y-%m-%d") return None except Exception as e: print(f"[NSE DATA] Error fetching expiry for {symbol}: {e}") return None

def get_option_chain(symbol): """ Get full option chain for the symbol """ try: url = f"{NSE_BASE_URL}/option-chain-indices?symbol={symbol.upper()}" response = requests.get(url, headers=HEADERS, timeout=10) data = response.json() records = data.get("records", {}) option_data = records.get("data", []) flat_chain = []

for item in option_data:
        strike = item.get("strikePrice")
        ce_data = item.get("CE")
        pe_data = item.get("PE")

        if ce_data:
            flat_chain.append({
                "strike": strike,
                "type": "CE",
                "last_price": ce_data.get("lastPrice", 0),
                "oi": ce_data.get("openInterest", 0)
            })

        if pe_data:
            flat_chain.append({
                "strike": strike,
                "type": "PE",
                "last_price": pe_data.get("lastPrice", 0),
                "oi": pe_data.get("openInterest", 0)
            })

    return flat_chain
except Exception as e:
    print(f"[NSE DATA] Error fetching option chain for {symbol}: {e}")
    return []

