import os

# Capital and risk config
CAPITAL = float(os.getenv("CAPITAL", 250000))
MAX_PREMIUM = float(os.getenv("MAX_PREMIUM", 150))

# LIVE or BACKTEST mode
STRATEGY_MODE = os.getenv("STRATEGY_MODE", "LIVE")

# Supported symbols: Comma-separated string in Render env like: BANKNIFTY,SENSEX,NIFTY
SYMBOLS = os.getenv("SYMBOLS", "BANKNIFTY,NIFTY,SENSEX").split(",")
