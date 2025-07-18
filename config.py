# config.py

CAPITAL = 220000                           # Updated capital
MAX_PREMIUM = 150                          # Max premium for OTM selection
STRATEGY_MODE = "LIVE"                     # "LIVE" or "BACKTEST"
SYMBOLS = ["BANKNIFTY", "NIFTY", "SENSEX"] # Indices to trade
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
