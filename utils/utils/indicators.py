import yfinance as yf
import pandas as pd
import numpy as np

def calculate_indicators(symbol, timeframe="1minute", mode="expiry"):
    interval = "1m" if timeframe == "1minute" else "3m"
    lookback = "1d"  # Fetch today's data

    yf_symbol = "^NSEBANK" if "BANKNIFTY" in symbol else "^NSEI" if "NIFTY" in symbol else "^BSESN"
    df = yf.download(yf_symbol, interval=interval, period=lookback, progress=False)

    if df.empty or len(df) < 30:
        return None, 0

    df["HL2"] = (df["High"] + df["Low"]) / 2
    df["OHLC4"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4

    # === Moving Averages ===
    df["MA_3"] = df["OHLC4"].rolling(3).mean()
    df["MA_9"] = df["OHLC4"].rolling(9).mean()
    df["MA_20"] = df["OHLC4"].rolling(20).mean()
    df["MA_50"] = df["High"].ewm(span=50, adjust=False).mean()
    df["MA_200_WMA"] = df["High"].rolling(200).mean()

    # === RSI and RSI MA ===
    delta = df["OHLC4"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(21).mean()
    avg_loss = loss.rolling(21).mean()
    rs = avg_gain / avg_loss
    df["RSI_21"] = 100 - (100 / (1 + rs))
    df["RSI_MA_9"] = df["RSI_21"].rolling(9).mean()
    df["RSI_MA_14"] = df["RSI_21"].rolling(14).mean()
    df["RSI_MA_26"] = df["RSI_21"].rolling(26).mean()

    # === Price Volume Strength ===
    df["Vol_Strength"] = df["Volume"] * df["Close"]

    # === Linear Regression Slope (Price) ===
    def lr_slope(series):
        x = np.arange(len(series))
        if len(series) < 2:
            return 0
        A = np.vstack([x, np.ones(len(x))]).T
        m, _ = np.linalg.lstsq(A, series, rcond=None)[0]
        return m

    df["LR_Slope"] = df["High"].rolling(21).apply(lr_slope, raw=True)

    latest = df.iloc[-1]

    # === 4-Step Confirmation ===
    conditions = [
        latest["Close"] > latest["MA_3"] > latest["MA_9"] > latest["MA_20"] > latest["MA_50"] > latest["MA_200_WMA"],
        latest["RSI_21"] > latest["RSI_MA_9"] > latest["RSI_MA_14"] > latest["RSI_MA_26"],
        latest["Vol_Strength"] > df["Vol_Strength"].rolling(20).mean().iloc[-1],
        latest["LR_Slope"] > 30,
    ]

    signal_strength = sum(conditions)

    direction = None
    if signal_strength >= 4:
        direction = "CE" if latest["Close"] > latest["MA_3"] else "PE"

    return direction, signal_strength
