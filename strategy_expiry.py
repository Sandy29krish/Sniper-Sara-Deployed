# strategy_expiry.py

def run_expiry_strategy():
    print("📈 Expiry strategy executed (placeholder).")
    # TODO: Add your expiry signal detection and execution logic here

# strategy_expiry.py

from nse_data import get_expiry_dates, get_spot_price, get_option_chain_data
from lot_manager import calculate_lot_size, filter_otm_option_chain
from telegram_bot import TelegramBot
from learning_engine import log_trade_learning
from datetime import datetime
import time
import json

def run_expiry_strategy(symbols=["BANKNIFTY", "NIFTY", "SENSEX"], capital=230000, lot_size=15, max_premium=60):
    telegram = TelegramBot()
    telegram.send_message(f"🚀 Sniper Expiry Strategy Started")

    for symbol in symbols:
        try:
            telegram.send_message(f"📡 Scanning {symbol}")

            expiry_list = get_expiry_dates(symbol)
            if not expiry_list:
                telegram.send_message(f"❌ No expiry data for {symbol}")
                continue

            expiry = expiry_list[0]
            spot_price = get_spot_price(symbol)
            if not spot_price:
                telegram.send_message(f"❌ Failed to fetch spot price for {symbol}")
                continue

            option_chain = get_option_chain_data(symbol, expiry)
            if not option_chain:
                telegram.send_message(f"❌ Option chain unavailable for {symbol}")
                continue

            # Determine direction from signal (placeholder)
            direction = detect_signal_direction(symbol)
            if not direction:
                telegram.send_message(f"⚠️ No signal for {symbol}, skipping.")
                continue

            otm_option = filter_otm_option_chain(option_chain, spot_price, direction, max_price=max_premium)
            if not otm_option:
                telegram.send_message(f"❌ No OTM option found for {symbol}")
                continue

            premium = otm_option["last_price"]
            strike = otm_option["strike"]

            lots, used_capital = calculate_lot_size(capital, premium, lot_size)
            if lots == 0:
                telegram.send_message(f"❌ Insufficient capital for {symbol}")
                continue

            # Entry Alert
            entry_time = datetime.now().strftime("%H:%M:%S")
            telegram.send_message(
                f"✅ Entry\n{symbol} | {strike} {direction}\nPremium: {premium} | Lots: {lots}\nCapital Used: ₹{used_capital}\nTime: {entry_time}"
            )

            time.sleep(2)

            # Simulated Exit
            exit_price = round(premium * 1.75, 2)
            exit_time = datetime.now().strftime("%H:%M:%S")
            telegram.send_message(
                f"💰 Exit\n{symbol} | {strike} {direction}\nExit Price: {exit_price}\nTime: {exit_time}"
            )

            log_trade_learning({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "strategy": "expiry",
                "symbol": symbol,
                "signal_strength": "strong",
                "entry_reason": "All conditions met",
                "exit_reason": "Target hit",
                "pnl_percent": 75,
                "fake_breakout": False,
                "theta_decay_impact": "low"
            })

            telegram.send_message(f"📘 {symbol} trade logged for learning.")

        except Exception as e:
            telegram.send_message(f"❌ Error in {symbol} processing: {str(e)}")
