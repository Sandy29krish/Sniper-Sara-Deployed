import os

# Strategy configuration
CAPITAL = float(os.getenv("CAPITAL", 250000))           # Example default capital
MAX_PREMIUM = float(os.getenv("MAX_PREMIUM", 150))      # Max premium for OTM option
STRATEGY_MODE = os.getenv("STRATEGY_MODE", "LIVE")      # LIVE or BACKTEST
SYMBOLS = os.getenv("SYMBOLS", "BANKNIFTY,NIFTY").split(",")  # Comma-separated symbols
