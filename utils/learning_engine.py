import json
import os
from datetime import datetime

LEARNING_LOG = "learning_log.json"

def learn_from_trade(symbol, direction, entry_price, exit_price, reason, strategy="expiry"):
    result = "WIN" if exit_price > entry_price else "LOSS"
    delta = round(exit_price - entry_price, 2)
    percentage_change = round((exit_price - entry_price) / entry_price * 100, 2)

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategy": strategy,
        "symbol": symbol,
        "direction": direction,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "result": result,
        "return_%": percentage_change,
        "reason": reason,
        "delta": delta
    }

    if not os.path.exists(LEARNING_LOG):
        with open(LEARNING_LOG, "w") as f:
            json.dump([record], f, indent=2)
    else:
        with open(LEARNING_LOG, "r+") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=2)
