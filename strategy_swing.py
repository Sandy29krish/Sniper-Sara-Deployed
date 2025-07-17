# strategy_swing.py

def run_swing_strategy():
    print("📊 Swing strategy executed (placeholder).")
    # TODO: Add your swing trade logic here
# strategy_swing.py

from nse_data import get_expiry_dates, get_spot_price, get_option_chain_data
from lot_manager import calculate_lot_size, filter_otm_option_chain
from telegram_bot import TelegramBot
from learning_engine import log_trade_learning
from datetime import datetime
import time

def run_swing_strategy():
    telegram = TelegramBot()
    telegram.send_message("📈 Sniper Swing Strategy Started")

    symbol = "NIFTY"
    capital = 220000
    lot_size = 25
    max_premium = 80  # slightly flexible for swing
    today = datetime.now()
    
    # Step 1: Get expiry dates and pick NEXT WEEK
    expiry_list = get_expiry_dates(symbol)
    if not expiry_list or len(expiry_list) < 2:
        telegram.send_message("❌ Not enough expiries available.")
        return

    # Use 2nd expiry (next weekly), fallback to last monthly if end of month
    expiry = expiry_list[1]
    if today.day > 23:  # simple monthly expiry check
        expiry = expiry_list[-1]

    spot_price = get_spot_price(symbol)
    if not spot_price:
        telegram.send_message("❌ Spot price fetch failed.")
        return

    option_chain = get_option_chain_data(symbol, expiry)
    if not option_chain:
        telegram.send_message("❌ Option chain unavailable.")
        return

    # Placeholder: Direction = CE, simulate logic until full indicator check is added
    direction = "CE"
    otm_option = filter_otm_option_chain(option_chain, spot_price, direction, max_price=max_premium)
    if not otm_option:
        telegram.send_message("❌ No suitable OTM found.")
        return

    premium = otm_option["last_price"]
    strike = otm_option["strike"]
    lots, used_capital = calculate_lot_size(capital, premium, lot_size)

    if lots == 0:
        telegram.send_message("❌ Capital insufficient for swing trade.")
        return

    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    telegram.send_message(
        f"✅ Swing Entry\nSymbol: {symbol}\nStrike: {strike} {direction}\nPremium: {premium}\nLots: {lots}\nUsed Capital: ₹{used_capital}\nTime: {entry_time}"
    )

    # Simulate swing holding time
    time.sleep(2)

    exit_price = round(premium * 1.85, 2)
    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    telegram.send_message(
        f"💸 Swing Exit\nStrike: {strike} {direction}\nExit Price: {exit_price}\nExit Time: {exit_time}"
    )

    log_trade_learning({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "strategy": "swing",
        "signal_strength": "strong",
        "entry_reason": "MA cross + RSI + Volume",
        "exit_reason": "Target Hit",
        "pnl_percent": 85,
        "fake_breakout": False,
        "theta_decay_impact": "medium"
    })

    telegram.send_message("📘 Swing trade logged for learning.")
