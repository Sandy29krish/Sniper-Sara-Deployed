# strategy_swing.py

import datetime
from utils.nse_data import get_option_chain, get_index_future_price
from utils.lot_manager import calculate_lot_size, filter_otm_option_chain
from utils.learning_engine import log_learning
from utils.trade_logger import log_trade
from utils.telegram_bot import send_telegram_message
from utils.indicator_utils import check_all_swing_conditions

CAPITAL = 220000
INDEX_LIST = ["BANKNIFTY", "NIFTY", "SENSEX"]
LOT_SIZE = {"BANKNIFTY": 35, "NIFTY": 75, "SENSEX": 10}

def run_swing_strategy():
    now = datetime.datetime.now()
    if now.hour < 9 or now.hour > 15:
        return

    for index in INDEX_LIST:
        try:
            print(f"[Swing] Checking swing setup for {index}")

            future_price = get_index_future_price(index)
            if not future_price:
                send_telegram_message(f"⚠️ [Swing] No future price for {index}")
                continue

            # Check 10-min chart for build-up, confirm on 15-min
            signal_data = check_all_swing_conditions(index)

            if not signal_data or not signal_data.get("strong_signal"):
                print(f"[Swing] No strong signal for {index}")
                continue

            if not signal_data.get("closed_above_all_mas"):
                print(f"[Swing] Waiting for candle close above MAs on 15-min")
                continue

            direction = signal_data.get("direction")  # "CE" or "PE"
            expiry_date = signal_data.get("expiry")  # Next week/month expiry

            option_chain = get_option_chain(index)
            otm_option = filter_otm_option_chain(option_chain, future_price, direction, max_price=60)

            if not otm_option:
                send_telegram_message(f"⚠️ [Swing] No valid OTM option for {index}")
                continue

            premium = otm_option["last_price"]
            strike = otm_option["strike"]

            lots, capital_used = calculate_lot_size(CAPITAL, premium, index)
            if lots == 0:
                send_telegram_message(f"❌ [Swing] Insufficient capital for {index}")
                continue

            entry = {
                "symbol": index,
                "direction": direction,
                "strike": strike,
                "premium": premium,
                "expiry": expiry_date,
                "lots": lots,
                "capital_used": capital_used,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "strategy": "SWING"
            }

            send_telegram_message(
                f"✅ [SWING ENTRY]\n{index} {direction} {strike} @ ₹{premium}\nLots: {lots} | Expiry: {expiry_date}"
            )
            log_trade(entry)
            log_learning(entry, result="PENDING")

        except Exception as e:
            print(f"[Swing] Error in strategy: {e}")
            send_telegram_message(f"🚨 [Swing] Error in {index} - {e}")
