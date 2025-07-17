# lot_manager.py

def calculate_lot_size(capital, premium, lot_multiplier=15):
    """
    Calculates number of lots that can be bought based on available capital and premium.
    Assumes 1 lot = 15 quantity for BANKNIFTY, NIFTY, or SENSEX

    Returns:
        (lots, capital_used)
    """
    try:
        lot_cost = premium * lot_multiplier
        lots = int(capital // lot_cost)
        used_capital = lots * lot_cost
        return lots, used_capital
    except Exception as e:
        print(f"[Lot Manager] Error calculating lot size: {e}")
        return 0, 0

def filter_otm_option_chain(option_chain, spot_price, direction, max_price=60):
    """
    Filter OTM strike closest to spot price with premium < max_price
    and 100-point strike gap for expiry logic
    """
    try:
        otm_options = []
        for option in option_chain:
            strike = option.get("strike")
            last_price = option.get("last_price")
            if not strike or not last_price:
                continue

            if direction == "CE" and strike > spot_price and last_price <= max_price and (strike - spot_price) % 100 == 0:
                otm_options.append(option)
            elif direction == "PE" and strike < spot_price and last_price <= max_price and (spot_price - strike) % 100 == 0:
                otm_options.append(option)

        if not otm_options:
            return None

        sorted_options = sorted(otm_options, key=lambda x: abs(x["strike"] - spot_price))
        return sorted_options[0] if sorted_options else None

    except Exception as e:
        print(f"[Lot Manager] Error filtering OTM option chain: {e}")
        return None
