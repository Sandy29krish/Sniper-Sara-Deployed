def calculate_lot_size(symbol, capital, premium):
    lots_per_symbol = {
        "BANKNIFTY": 30,
        "NIFTY": 75,
        "SENSEX": 10
    }

    symbol_upper = symbol.upper()
    if symbol_upper not in lots_per_symbol:
        raise ValueError(f"Unknown symbol '{symbol}' — no lot size defined")

    lot_size = lots_per_symbol[symbol_upper]
    max_lots = capital // (premium * lot_size)
    return max(1, int(max_lots))
