import math
from config import CAPITAL, MAX_PREMIUM, SYMBOL_LOT_SIZE

def calculate_lot_size(symbol, premium):
    """
    Calculates number of lots based on capital and max premium.
    Falls back to fixed lot size if capital constraint is exceeded.
    """
    lot_size = SYMBOL_LOT_SIZE.get(symbol.upper(), 25)  # Default to 25 if not defined
    cost_per_lot = premium * lot_size

    if cost_per_lot == 0:
        return 0

    max_lots = CAPITAL // cost_per_lot
    if max_lots == 0:
        return 1  # Minimum 1 lot even if capital is low

    return int(max_lots)

def filter_otm_option_chain(option_chain, direction, spot_price):
    """
    Filters and returns the next 100-point OTM strike based on direction.
    """
    otm_options = []

    for option in option_chain:
        strike = option.get("strikePrice")
        if not strike:
            continue

        if direction == "CE" and strike > spot_price:
            otm_options.append(option)
        elif direction == "PE" and strike < spot_price:
            otm_options.append(option)

    # Sort by distance from spot
    otm_options = sorted(otm_options, key=lambda x: abs(x["strikePrice"] - spot_price))

    return otm_options[0] if otm_options else None
