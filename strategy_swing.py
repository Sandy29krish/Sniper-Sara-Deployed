import time
from utils.indicators import calculate_indicators
from utils.lot_manager import calculate_lot_size, filter_otm_option_chain
from utils.nse_data import fetch_nse_option_chain, get_future_price, get_next_swing_expiry
from utils.learning_engine import learn_from_trade
from utils.telegram_commands import send_telegram_message
from utils.trade_logger import log_trade
from utils.ai_assistant import explain_trade, should_enter_trade
from config import CAPITAL, MAX_PREMIUM, SYMBOLS, STRATEGY_MODE

def run_swing_strategy():
    print("[Swing Strategy] Initializing...")

    for symbol in SYMBOLS:
        try:
            expiry_date = get_next_swing_expiry(symbol)
            future_price = get_future_price(symbol)
            print(f"[{symbol}] Swing Expiry: {expiry_date}, Futures: {future_price}")

            # Use 15-min timeframe for confirmed swing signal
            direction, signal_strength = calculate_indicators(symbol, timeframe="15minute", mode="swing")
            if not direction or signal_strength < 4:
                print(f"[{symbol}] No strong swing setup. Skipping.")
                continue

            current_conditions = {
                "symbol": symbol,
                "direction": direction,
                "signal_strength": signal_strength
            }

            ai_decision = should_enter_trade(current_conditions)
            if "NO" in ai_decision:
                print(f"[{symbol}] Rejected by AI: {ai_decision}")
                continue

            option_chain = fetch_nse_option_chain(symbol)
            selected_option = filter_otm_option_chain(option_chain, future_price, direction, MAX_PREMIUM, expiry_date)

            if not selected_option:
                print(f"[{symbol}] No valid OTM option found for swing.")
                continue

            strike = selected_option["strikePrice"]
            ltp = selected_option["lastPrice"]
            lots = calculate_lot_size(symbol, CAPITAL, ltp)

            indicators = {
                "above_200wma": True,
                "rsi_strong": True,
                "volume_spike": True,
                "slope_strong": True,
                "strength": signal_strength
            }

            reasoning = explain_trade(symbol, direction, indicators)

            send_telegram_message(
                f"📥 SWING ENTRY: {symbol} {direction} {strike} @ {ltp} | Lots: {lots}\n🧠 Reason: {reasoning}"
            )
            log_trade("SWING ENTRY", symbol, direction, strike, ltp, lots, STRATEGY_MODE)

            monitor_swing_trade(symbol, direction, strike, ltp, lots)

        except Exception as e:
            print(f"[Swing Strategy] Error: {e}")


def monitor_swing_trade(symbol, direction, strike, entry_price, lots):
    print(f"[Monitor] Monitoring swing position for {symbol} {strike}...")
    stoploss_hit = False
    full_exit = False
    reason = ""
    entry_time = time.time()

    while True:
        try:
            time.sleep(900)  # check every 15 minutes
            current_price = get_option_price(symbol, strike, direction)
            elapsed_minutes = (time.time() - entry_time) / 60

            if current_price <= entry_price * 0.70:
                stoploss_hit = True
                reason = "Swing SL Hit"

            elif current_price >= entry_price * 2.0:
                full_exit = True
                reason = "Swing Target Hit (200%)"

            elif elapsed_minutes >= 1440:  # 24 hours
                full_exit = True
                reason = "Swing Time Exit (24hr)"

            if stoploss_hit or full_exit:
                send_telegram_message(
                    f"🔴 SWING EXIT: {symbol} {direction} {strike} @ {current_price} ({reason})"
                )
                log_trade("SWING EXIT", symbol, direction, strike, current_price, lots, "LIVE", reason=reason)
                learn_from_trade(symbol, direction, entry_price, current_price, reason, strategy="swing")
                break

        except Exception as e:
            print(f"[Swing Monitor] Error: {e}")


def get_option_price(symbol, strike, direction):
    # TODO: Replace with live API logic
    return 60.0
