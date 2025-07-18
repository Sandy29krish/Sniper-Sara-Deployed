# config.py

# Trading Capital and Limits
CAPITAL = 230000  # Adjust this based on available funds
MAX_PREMIUM = 100  # Optional: Used for filtering strikes (if needed)

# Symbol List for Strategy Execution
SYMBOLS = ["BANKNIFTY", "NIFTY", "SENSEX"]

# Lot Sizes for Each Index
SYMBOL_LOT_SIZE = {
    "BANKNIFTY": 30,
    "NIFTY": 75,
    "SENSEX": 15
}

# Strategy Mode: "expiry" or "swing"
STRATEGY_MODE = "expiry"  # Change to "swing" for swing trading

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_telegram_chat_id_here"

# Expiry Fetching
NSE_BASE_URL = "https://www.nseindia.com"
NSE_INDEX_SYMBOLS = {
    "BANKNIFTY": "BANKNIFTY",
    "NIFTY": "NIFTY",
    "SENSEX": "SENSEX"
}

# Enable AI Assistant (Optional OpenAI Key)
OPENAI_ENABLED = True
OPENAI_API_KEY = "your_openai_api_key_here"

# Token Management
AUTO_REFRESH_TOKEN = True  # Set False if using manual access token
KITE_USER_ID = "your_kite_user_id"
KITE_PASSWORD = "your_kite_password"
KITE_TOTP_SECRET = "your_totp_secret"  # For auto-login
