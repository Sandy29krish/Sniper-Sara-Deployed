# trade_logger.py

import json
import os
from datetime import datetime

LOG_FILE = "trade_log.json"

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_log(log_data):
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

def log_trade(entry_type, index, direction, strike, qty, premium, status, reason=None):
    log_data = load_log()
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "index": index,
        "direction": direction,
        "strike": strike,
        "qty": qty,
        "premium": premium,
        "entry_type": entry_type,
        "status": status,
        "reason": reason or "",
    }
    log_data.append(log_entry)
    save_log(log_data)

def get_today_summary():
    log_data = load_log()
    today = datetime.now().strftime("%Y-%m-%d")
    trades_today = [t for t in log_data if t["timestamp"].startswith(today)]

    if not trades_today:
        return "📅 No trades executed today."

    summary = {}
    for trade in trades_today:
        symbol = trade["index"]
        if symbol not in summary:
            summary[symbol] = {"count": 0, "capital": 0}
        summary[symbol]["count"] += 1
        summary[symbol]["capital"] += float(trade["premium"]) * int(trade["qty"])

    response = "📊 Today's Trade Summary:\n"
    for symbol, stats in summary.items():
        response += f"\n📌 {symbol}:\n- Trades: {stats['count']}\n- Approx. Capital Used: ₹{stats['capital']:.2f}\n"
    
    return response
