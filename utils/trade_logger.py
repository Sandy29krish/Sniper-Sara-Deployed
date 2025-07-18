# utils/trade_logger.py

import json
from datetime import datetime
import os

LOG_FILE = "trade_log.json"

def log_trade(action, symbol, direction, strike, price, lots, mode, reason=""):
    trade = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "symbol": symbol,
        "direction": direction,
        "strike": strike,
        "price": price,
        "lots": lots,
        "mode": mode,
        "reason": reason
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(trade)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
