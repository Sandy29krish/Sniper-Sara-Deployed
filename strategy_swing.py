import time 
from utils.indicators import calculate_indicators 
from utils.lot_manager import calculate_lot_size, get_next_week_expiry_strike 
from utils.nse_data import get_future_price, get_expiry_date 
from utils.learning_engine import learn_from_trade 
from utils.telegram_bot import send_telegram_message 
from utils.trade_log import log_trade 
from config import CAPITAL, SYMBOLS, STRATEGY_MODE

def run_swing_strategy(): print("[Swing Strategy] Initializing...") for symbol in SYMBOLS: try: future_price = get_future_price(symbol) expiry_date = get_expiry_date(symbol, swing=True)  # next week's expiry print(f"[{symbol}] Swing Mode | Expiry: {expiry_date} | Futures: {future_price}")

direction, signal_strength = calculate_indicators(symbol, timeframe="15minute", mode="swing")
        if not direction or signal_strength < 4:
            print(f"[{symbol}] No strong signal. Skipping.")
            continue

        strike = get_next_week_expiry_strike(symbol, future_price, direction)
        entry_price = 60.0  # placeholder; replace with live premium fetch
        lots = calculate_lot_size(symbol, CAPITAL, entry_price)

        send_telegram_message(
            f"📥 Swing Entry: {symbol} {direction} {strike} @ {entry_price} | Lots: {lots}"
        )
        log_trade("ENTRY", symbol, direction, strike, entry_price, lots, STRATEGY_MODE)

        monitor_swing_trade(symbol, direction, strike, entry_price, lots)

    except Exception as e:
        print(f"[Swing Strategy] Error: {e}")

def monitor_swing_trade(symbol, direction, strike, entry_price, lots): print(f"[Swing Monitor] Watching {symbol} {strike}...") start_time = time.time() reason = ""

while True:
    try:
        time.sleep(600)  # 10-minute observation
        elapsed_minutes = (time.time() - start_time) / 60
        current_price = get_option_price(symbol, strike, direction)

        if current_price <= entry_price * 0.7:
            reason = "Stop Loss Hit"

        elif current_price >= entry_price * 2.0:
            reason = "Target Hit (200%)"

        elif elapsed_minutes >= 1440:  # 1-day holding
            reason = "Time-based Exit (EOD)"

        elif is_swing_reversal(symbol, direction):
            reason = "Reversal Detected"

        if reason:
            send_telegram_message(
                f"🔴 Swing Exit: {symbol} {direction} {strike} @ {current_price} ({reason})"
            )
            log_trade("FULL EXIT", symbol, direction, strike, current_price, lots, "LIVE", reason=reason)
            learn_from_trade(symbol, direction, entry_price, current_price, reason, strategy="swing")
            break

    except Exception as e:
        print(f"[Swing Monitor] Error: {e}")

=== Placeholders ===

def get_option_price(symbol, strike, direction): return 60.0  # Replace with live API call

def is_swing_reversal(symbol, direction): return False  # Replace with 2-candle pattern logic

