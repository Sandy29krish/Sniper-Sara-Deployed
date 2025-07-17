# learning_engine.py

import json
import os
from datetime import datetime

LEARNING_LOG_PATH = "learning_log.json"

def record_trade_learning(signal, outcome, notes=""):
    """
    Log the trade context and outcome into the learning log.
    """
    try:
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "signal": signal,  # e.g. all indicators snapshot
            "outcome": outcome,  # "win", "loss", "exit", "no_trade"
            "notes": notes
        }

        if not os.path.exists(LEARNING_LOG_PATH):
            with open(LEARNING_LOG_PATH, "w") as f:
                json.dump([entry], f, indent=4)
        else:
            with open(LEARNING_LOG_PATH, "r") as f:
                data = json.load(f)
            data.append(entry)
            with open(LEARNING_LOG_PATH, "w") as f:
                json.dump(data, f, indent=4)

        print(f"[Learning] Logged trade outcome: {outcome}")
    except Exception as e:
        print(f"[Learning Engine] Failed to log trade: {e}")


def analyze_past_failures():
    """
    Review past losses to find patterns – e.g., mild signals, low volume, etc.
    Returns: List of reasons if found common patterns
    """
    try:
        if not os.path.exists(LEARNING_LOG_PATH):
            print("[Learning] No learning log found.")
            return []

        with open(LEARNING_LOG_PATH, "r") as f:
            data = json.load(f)

        failure_patterns = {}
        for entry in data:
            if entry["outcome"] == "loss":
                reason = entry.get("notes", "unknown")
                failure_patterns[reason] = failure_patterns.get(reason, 0) + 1

        sorted_patterns = sorted(failure_patterns.items(), key=lambda x: x[1], reverse=True)
        return sorted_patterns

    except Exception as e:
        print(f"[Learning Engine] Error analyzing past failures: {e}")
        return []
