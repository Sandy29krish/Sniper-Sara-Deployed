import time 
from utils.indicators import calculate_indicators 
from utils.lot_manager import calculate_lot_size, filter_otm_option_chain 
from utils.nse_data import fetch_nse_option_chain, get_future_price, get_expiry_date 
from utils.learning_engine import learn_from_trade 
from utils.telegram_bot import send_telegram_message 
from utils.trade_log import log_trade 
from utils.ai_assistant import explain_trade, learn_from_mistake, should_enter_trade 
from config import CAPITAL, MAX_PREMIUM, SYMBOLS, STRATEGY_MODE

def run_expiry_strategy(): print("[Expiry Strategy] Initializing...") for symbol in SYMBOLS: try: expiry_date = get_expiry_date(symbol) future_price = get_future_price(symbol) print(f"[{symbol}] Expiry: {expiry_date}, Future Price: {future_price}")

direction, signal_strength = calculate_indicators(symbol, timeframe="1minute", mode="expiry")
        if not direction or signal_strength < 4:
            print(f"[{symbol}] No strong signal or direction. Skipping.")
            continue

        current_conditions = {
            "symbol": symbol,
            "direction": direction,
            "signal_strength": signal_strength
        }

        ai_check = should_enter_trade(current_conditions)
        if "NO" in ai_check:
            print(f"[{symbol}] AI rejected entry: {ai_check}")
            continue

        option_chain = fetch_nse_option_chain(symbol)
        selected_option = filter_otm_option_chain(
            option_chain, future_price, direction, MAX_PREMIUM
        )
        if not selected_option:
            print(f"[{symbol}] No suitable OTM option found.")
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
            f"📥 Entry: {symbol} {direction} {strike} @ {ltp} | Lots: {lots}\n🤖 Reason: {reasoning}"
        )
        log_trade("ENTRY", symbol, direction, strike, ltp, lots, STRATEGY_MODE)

        monitor_trade(symbol, direction, strike, ltp, lots)

    except Exception as e:
        print(f"[Expiry Strategy] Error: {e}")

def monitor_trade(symbol, direction, strike, entry_price, lots): print(f"[Monitor] Monitoring {symbol} {strike}...") start_time = time.time() stoploss_hit = False full_exit_done = False reason = ""

while True:
    try:
        time.sleep(60)  # 1-minute candle wait
        elapsed_minutes = (time.time() - start_time) / 60
        current_price = get_option_price(symbol, strike, direction)

        if current_price <= entry_price * 0.65:
            stoploss_hit = True
            reason = "Stop Loss Hit"

        elif current_price >= entry_price * 1.85:
            send_telegram_message(
                f"💰 Tier-1 Profit Booking: {symbol} {direction} {strike} @ {current_price} (185%)"
            )
            log_trade("PARTIAL EXIT", symbol, direction, strike, current_price, lots // 2, "LIVE", reason="Tier-1 Target Hit")

        elif current_price >= entry_price * 2.2:
            full_exit_done = True
            reason = "Tier-2 Target Hit (220%)"

        elif elapsed_minutes >= 195:
            full_exit_done = True
            reason = "Time-based Exit (3:15 PM)"

        elif is_reversal_detected(symbol, direction):
            full_exit_done = True
            reason = "Reversal Detected"

        if stoploss_hit or full_exit_done:
            send_telegram_message(
                f"🔴 Exit: {symbol} {direction} {strike} @ {current_price} ({reason})"
            )
            log_trade(
                "FULL EXIT", symbol, direction, strike, current_price,
                lots if stoploss_hit else lots // 2, "LIVE", reason=reason
            )
            if stoploss_hit:
                context = {
                    "entry_price": entry_price,
                    "exit_price": current_price,
                    "reason": reason,
                    "duration": elapsed_minutes
                }
                insight = learn_from_mistake(symbol, context, result="LOSS")
                send_telegram_message(f"🧠 AI Insight: {insight}")

            learn_from_trade(symbol, direction, entry_price, current_price, reason, strategy="expiry")
            break

    except Exception as e:
        print(f"[Monitor] Error: {e}")

=== Placeholder functions ===

def get_option_price(symbol, strike, direction): # TODO: Replace with live API to fetch current premium return 60.0

def is_reversal_detected(symbol, direction): # TODO: Replace with proper logic based on 2-candle structure return False

