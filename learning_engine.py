# learning_engine.py

import json
import os
from datetime import datetime

LEARNING_LOG_FILE = "learning_log.json"

def log_trade_learning(trade_context: dict):
    """
    Store insights about trade setups and outcomes.
    Example context:
    {
        "date": "2025-07-17",
        "strategy": "expiry",
        "signal_strength": "strong",
        "entry_reason": "RSI + MA + LR Slope",
        "exit_reason": "Target hit",
        "pnl_percent": 85,
        "fake_breakout": False,
        "theta_decay_impact": "low"
    }
    """
    if not os.path.exists(LEARNING_LOG_FILE):
        with open(LEARNING_LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LEARNING_LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append(trade_context)

    with open(LEARNING_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def analyze_learning():
    """
    Reads past learning log and prints summarized insights.
    """
    if not os.path.exists(LEARNING_LOG_FILE):
        print("📭 No learning data found.")
        return

    with open(LEARNING_LOG_FILE, "r") as f:
        logs = json.load(f)

    total = len(logs)
    fake_breakouts = sum(1 for log in logs if log.get("fake_breakout"))
    avg_pnl = sum(log.get("pnl_percent", 0) for log in logs) / total if total else 0

    print(f"📊 Total trades logged: {total}")
    print(f"⚠️ Fake breakouts: {fake_breakouts}")
    print(f"💰 Average PnL: {avg_pnl:.2f}%")

    # Optional: flag signals with repeat patterns
    strong_success = [log for log in logs if log["signal_strength"] == "strong" and log["pnl_percent"] > 50]
    print(f"✅ Strong signals with >50% PnL: {len(strong_success)}")


# Example Usage (inside expiry/swing strategy):
# from learning_engine import log_trade_learning
# log_trade_learning({
#     "date": datetime.now().strftime("%Y-%m-%d"),
#     "strategy": "expiry",
#     "signal_strength": "strong",
#     "entry_reason": "MA cross + RSI + Volume",
#     "exit_reason": "Reversal",
#     "pnl_percent": -40,
#     "fake_breakout": True,
#     "theta_decay_impact": "high"
# })

