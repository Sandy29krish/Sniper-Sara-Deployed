import json
import os
from datetime import datetime

LOG_FILE = "trade_log.json"

def log_trade(action, symbol, direction, strike, price, lots, mode, reason=""):
    trade = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,  # ENTRY, PARTIAL EXIT, FULL EXIT
        "symbol": symbol,
        "direction": direction,
        "strike": strike,
        "price": price,
        "lots": lots,
        "mode": mode,  # LIVE or BACKTEST
        "reason": reason
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([trade], f, indent=2)
    else:
        with open(LOG_FILE, "r+") as f:
            data = json.load(f)
            data.append(trade)
            f.seek(0)
            json.dump(data, f, indent=2)
