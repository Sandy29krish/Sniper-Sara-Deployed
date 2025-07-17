import math

def filter_otm_option_chain(option_chain, future_price, direction, max_premium):
    """
    Filters and selects the next OTM strike based on the direction, future price,
    and maximum premium allowed.
    """
    try:
        symbol = option_chain["symbol"]
        data = option_chain["records"]["data"]
        
        # Strike gap logic
        gap = 50 if "NIFTY" in symbol else 100
        target_strike = math.ceil(future_price / gap) * gap if direction == "CE" else math.floor(future_price / gap) * gap

        # Scan option chain
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
        print(f"[OTM Filter] Error: {e}")
        return None
