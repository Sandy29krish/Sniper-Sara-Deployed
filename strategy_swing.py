strategy_swing.py

import datetime 
from utils.indicators import calculate_indicators 
from utils.helpers import check_entry_conditions, check_exit_conditions 
from utils.lot_manager import calculate_lot_size 
from utils.nse_data import get_future_price, get_option_chain, get_next_swing_expiry 
from trade_logger import log_trade

def run_swing_strategy(index_symbol, capital): print(f"[Swing Strategy] Running swing strategy for {index_symbol}")

try:
    # Get current future price
    future_price = get_future_price(index_symbol)
    if not future_price:
        print("[Swing Strategy] Unable to fetch future price.")
        return

    # Get historical data and calculate indicators (10min & 15min TF handled internally)
    signal_data = calculate_indicators(index_symbol, timeframe='15m', lookback=100)

    if not signal_data or len(signal_data) < 2:
        print("[Swing Strategy] Not enough data for signal check.")
        return

    latest = signal_data[-1]
    previous = signal_data[-2]

    # Check entry conditions (strong signal + candle closed above MAs + OI/volume/momentum confirmation)
    if check_entry_conditions(latest, previous, strategy='swing'):
        direction = "CE" if latest['trend'] == 'bullish' else "PE"
        expiry = get_next_swing_expiry(index_symbol)

        option_chain = get_option_chain(index_symbol, expiry)
        if not option_chain:
            print("[Swing Strategy] Option chain unavailable.")
            return

        from utils.lot_manager import filter_otm_option_chain
        selected_option = filter_otm_option_chain(option_chain, future_price, direction)

        if not selected_option:
            print("[Swing Strategy] No suitable OTM option found.")
            return

        strike = selected_option['strike']
        premium = selected_option['last_price']
        lots, capital_used = calculate_lot_size(capital, premium, index_symbol)

        if lots == 0:
            print("[Swing Strategy] Insufficient capital for trade.")
            return

        log_trade("ENTRY", index_symbol, direction, strike, premium, capital_used, "LIVE", reason="Swing Signal Confirmed")
        print(f"[Swing Strategy] Placing order: {lots} lots of {index_symbol} {strike}{direction} at {premium}")

        # Simulate or execute order here using broker API

    else:
        print("[Swing Strategy] Entry conditions not met.")

except Exception as e:
    print(f"[Swing Strategy] Error: {e}")

