# utils/lot_manager.py

def calculate_lot_size(symbol, capital, premium):
    """
    Calculate number of lots based on capital and per-lot premium.
    Follows minimum lot sizing as:
    - BANKNIFTY: 30
    - NIFTY: 75
    - SENSEX: 10
    """

    lot_sizes = {
        "BANKNIFTY": 30,
        "NIFTY": 75,
        "SENSEX": 10
    }

    lot_size = lot_sizes.get(symbol.upper(), 25)  # Default fallback 25
    total_cost_per_lot = lot_size * premium

    if total_cost_per_lot == 0:
        return 0

    max_lots = int(capital // total_cost_per_lot)
    return max(lot_size, max_lots * lot_size)


def filter_otm_option_chain(option_chain, future_price, direction, max_premium):
    """
    Filters OTM options based on direction and premium constraints.
    Picks the next OTM option (100-point gap) with premium ≤ max_premium.
    """

    try:
        strike_gap = 100  # Can be made dynamic if needed

        if direction == "CE":
            otm_strike = ((future_price // strike_gap) + 1) * strike_gap
        elif direction == "PE":
            otm_strike = ((future_price // strike_gap) - 1) * strike_gap
        else:
            return None

        for option in option_chain:
            if option["strikePrice"] == otm_strike and option["type"] == direction:
                if option["lastPrice"] <= max_premium:
                    return option

    except Exception as e:
        print(f"[Lot Manager] Error filtering option: {e}")

    return None
