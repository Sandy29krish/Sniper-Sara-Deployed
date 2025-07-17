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


def run_expiry_strategy():
    telegram = TelegramBot()
    telegram.send_message("🚀 Sniper Expiry Strategy Started")

    symbol = "BANKNIFTY"
    capital = 230000
    lot_size = 15
    max_premium = 60

    # Step 1: Get expiry and spot price
    expiry_list = get_expiry_dates(symbol)
    if not expiry_list:
        telegram.send_message("❌ No expiry data found.")
        return

    expiry = expiry_list[0]
    spot_price = get_spot_price(symbol)
    if not spot_price:
        telegram.send_message("❌ Spot price fetch failed.")
        return

    option_chain = get_option_chain_data(symbol, expiry)
    if not option_chain:
        telegram.send_message("❌ Option chain data unavailable.")
        return

    # Step 2: Filter next OTM strike
    direction = "CE"  # Placeholder for signal direction
    otm_option = filter_otm_option_chain(option_chain, spot_price, direction, max_price=max_premium)
    if not otm_option:
        telegram.send_message("❌ No suitable OTM option found.")
        return

    premium = otm_option["last_price"]
    strike = otm_option["strike"]

    lots, used_capital = calculate_lot_size(capital, premium, lot_size)
    if lots == 0:
        telegram.send_message("❌ Capital insufficient for trade.")
        return

    entry_time = datetime.now().strftime("%H:%M:%S")
    telegram.send_message(
        f"✅ Entry Triggered\nSymbol: {symbol}\nStrike: {strike} {direction}\nPremium: {premium}\nLots: {lots}\nCapital Used: ₹{used_capital}\nTime: {entry_time}"
    )

    # Simulate execution delay
    time.sleep(2)

    # Step 3: Simulate Exit
    exit_price = round(premium * 1.75, 2)  # Simulated 75% profit
    exit_time = datetime.now().strftime("%H:%M:%S")
    telegram.send_message(
        f"💰 Exit Triggered\nStrike: {strike} {direction}\nExit Price: {exit_price}\nTime: {exit_time}"
    )

    # Step 4: Learning Log
    log_trade_learning({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "strategy": "expiry",
        "signal_strength": "strong",
        "entry_reason": "All conditions met",
        "exit_reason": "Target hit",
        "pnl_percent": 75,
        "fake_breakout": False,
        "theta_decay_impact": "low"
    })

    telegram.send_message("📘 Trade logged for learning.")
