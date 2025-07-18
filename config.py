# config.py

CAPITAL = 230000  # Adjust based on your capital
MAX_PREMIUM = 120  # Avoid options > this premium

# Lot size for each index
LOT_SIZE = {
    "BANKNIFTY": 30,
    "NIFTY": 75,
    "SENSEX": 10
}

# Strategy mode
STRATEGY_MODE = "expiry"  # or "swing"

# Telegram Bot Settings (Optional, if you're using .env, leave blank here)
TELEGRAM_TOKEN = ""  # keep blank if using env vars
TELEGRAM_CHAT_ID = ""
