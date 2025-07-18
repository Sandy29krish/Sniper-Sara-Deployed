# utils/lot_manager.py

from config import CAPITAL, MAX_PREMIUM, LOT_SIZE

def calculate_lot_size(symbol):
    lot_size = LOT_SIZE.get(symbol, 0)
    if not lot_size:
        raise ValueError(f"Unknown symbol: {symbol}")
    capital_per_lot = 10000
    total_lots = CAPITAL // (capital_per_lot * lot_size)
    return total_lots if total_lots > 0 else 1

def filter_otm_option_chain(option_chain, future_price, direction):
    strike_gap = 100
    target_strike = None
    available_strikes = sorted([entry["strikePrice"] for entry in option_chain])

    if direction == "CE":
        target_strike = next((strike for strike in available_strikes if strike > future_price), None)
    elif direction == "PE":
        target_strike = next((strike for strike in reversed(available_strikes) if strike < future_price), None)

    if not target_strike:
        print("[Lot Manager] No suitable strike found.")
        return None

    for entry in option_chain:
        if entry["strikePrice"] == target_strike:
            return entry
    return None
