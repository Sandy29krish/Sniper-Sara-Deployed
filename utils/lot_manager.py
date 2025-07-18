import math

def filter_otm_option_chain(option_chain, future_price, direction, max_premium):
    """
    Filters next OTM strike based on future price, direction, and strike gap.
    """
    try:
        symbol = option_chain["symbol"]
        data = option_chain["records"]["data"]

        # Define strike gap per symbol
        if "NIFTY" in symbol.upper():
            gap = 50
        elif "SENSEX" in symbol.upper():
            gap = 100
        else:
            gap = 100  # Default BANKNIFTY

        target_strike = (
            math.ceil(future_price / gap) * gap if direction == "CE"
            else math.floor(future_price / gap) * gap
        )

        for record in data:
            strike = record["strikePrice"]

            if direction == "CE" and strike >= target_strike:
                if "CE" in record and record["CE"]["lastPrice"] <= max_premium:
                    return {
                        "strikePrice": strike,
                        "lastPrice": record["CE"]["lastPrice"]
                    }

            elif direction == "PE" and strike <= target_strike:
                if "PE" in record and record["PE"]["lastPrice"] <= max_premium:
                    return {
                        "strikePrice": strike,
                        "lastPrice": record["PE"]["lastPrice"]
                    }

        return None

    except Exception as e:
        print(f"[OTM Filter Error] {e}")
        return None


def calculate_lot_size(symbol, capital, premium):
    lots_per_symbol = {
        "BANKNIFTY": 30,
        "NIFTY": 75,
        "SENSEX": 10
    }
    default_lot = 25
    lot_size = lots_per_symbol.get(symbol.upper(), default_lot)
    max_lots = capital // (premium * lot_size)
    return max(1, int(max_lots))
