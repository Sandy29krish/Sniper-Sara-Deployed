# strategy_expiry.py

import time
from utils.indicators import calculate_indicators
from utils.lot_manager import calculate_lot_size, filter_otm_option_chain
from utils.nse_data import fetch_nse_option_chain, get_future_price, get_expiry_date
from utils.learning_engine import learn_from_trade
from utils.telegram_bot import send_telegram_message
from utils.trade_log import log_trade
from config import CAPITAL, MAX_PREMIUM, SYMBOLS, STRATEGY_MODE


def run_expiry_strategy():
    print("[Expiry Strategy] Initializing...")
    for symbol in SYMBOLS:
        try:
            expiry_date = get_expiry_date(symbol)
            future_price = get_future_price(symbol)
            print(f"[{symbol}] Expiry: {expiry_date}, Future Price: {future_price}")

            direction, signal_strength = calculate_indicators(symbol, timeframe="1minute", mode="expiry")
            if not direction or signal_strength < 3:
                print(f"[{symbol}] No strong signal or direction yet. Skipping.")
                continue

            option_chain = fetch_nse_option_chain(symbol)
            otm_option = filter_otm_option_chain(option_chain, future_price, direction, MAX_PREMIUM)
            if not otm_option:
                print(f"[{symbol}] No valid OTM option found.")
                continue

            premium = otm_option["last_price"]
            strike = otm_option["strike"]
            lots, capital_used = calculate_lot_size(CAPITAL, premium, symbol)
            if lots == 0:
                print(f"[{symbol}] Not enough capital for even 1 lot.")
                continue

            message = f"\n🚀 Expiry Signal for {symbol}\nDirection: {direction}\nStrike: {strike}\nPremium: {premium}\nLots: {lots}\nCapital Used: ₹{capital_used}"
            send_telegram_message(message)

            log_trade(symbol, direction, strike, premium, lots, "ENTRY", strategy="expiry")

            monitor_trade(symbol, direction, strike, premium, lots)

        except Exception as e:
            print(f"[Expiry Strategy] Error processing {symbol}: {e}")


def monitor_trade(symbol, direction, strike, entry_price, lots):
    try:
        stoploss_hit = False
        partial_exit_done = False
        full_exit_done = False
        entry_time = time.time()

        while True:
            time.sleep(30)  # Poll every 30 seconds

            current_price = get_option_price(symbol, strike, direction)
            elapsed_minutes = (time.time() - entry_time) / 60

            if current_price <= entry_price * 0.65:
                stoploss_hit = True
                reason = "SL Hit (35% drop)"

            elif not partial_exit_done and entry_price * 1.85 <= current_price <= entry_price * 2.0:
                partial_exit_done = True
                reason = "Tier-1 Target Hit (185-200%)"
                send_telegram_message(f"🔔 Partial Exit: {symbol} {direction} {strike} @ {current_price} ({reason})")
                log_trade(symbol, direction, strike, current_price, lots // 2, "PARTIAL EXIT", strategy="expiry")

            elif partial_exit_done and current_price >= entry_price * 2.2:
                full_exit_done = True
                reason = "Tier-2 Target Hit (220%)"

            elif elapsed_minutes >= 195:  # 3:15 PM mark
                full_exit_done = True
                reason = "Time-based Exit (3:15 PM)"

            elif is_reversal_detected(symbol, direction):
                full_exit_done = True
                reason = "Reversal Detected"

            if stoploss_hit or full_exit_done:
                send_telegram_message(f"🔴 Exit: {symbol} {direction} {strike} @ {current_price} ({reason})")
                log_trade(symbol, direction, strike, current_price, lots if stoploss_hit else lots // 2, "FULL EXIT", strategy="expiry")
                learn_from_trade(symbol, direction, entry_price, current_price, reason, strategy="expiry")
                break

    except Exception as e:
        print(f"[Monitor] Error: {e}")


def get_option_price(symbol, strike, direction):
    # Placeholder for live price fetch
    return 60.0


def is_reversal_detected(symbol, direction):
    # Placeholder for reversal logic based on 2-candle close below
    return False
