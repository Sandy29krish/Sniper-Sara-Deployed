from config import CAPITAL, MAX_PREMIUM, SYMBOLS

SYMBOL_LOT_SIZE = {"BANKNIFTY": 30, "NIFTY": 75, "SENSEX": 10}

def calculate_lot_size(symbol, capital, premium):
    lot_size = SYMBOL_LOT_SIZE.get(symbol.upper(), 1)
    # Example: invest up to 1% of capital per trade
    budget = capital * 0.01
    quantity = int(budget / premium)
    return max(1, quantity // lot_size) * lot_size

def filter_otm_option_chain(chain, future_price, direction, max_premium):
    # Placeholder: filter for strikes near future_price and LTP < max_premium
    # Return selected option dict or None
    return next((opt for opt in chain 
                 if abs(opt["strikePrice"] - future_price) < 500 and opt["lastPrice"] <= max_premium), None)
