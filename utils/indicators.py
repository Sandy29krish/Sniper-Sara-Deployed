import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.kite_instance import kite  # ✅ Already imported correctly

def calculate_indicators(symbol, timeframe="1minute", mode="expiry"):
    interval = "minute" if timeframe == "1minute" else "3minute"
    duration = 1  # 1 day

    # Define instrument token map
    instrument_map = {
        "BANKNIFTY": "NSE:NIFTYBANK",
        "NIFTY": "NSE:NIFTY 50",
        "SENSEX": "BSE:SENSEX"
    }

    instrument = instrument_map.get(symbol.upper())
    if not instrument:
        return None, 0

    # Get historical data
    to_date = datetime.now()
    from_date = to_date - timedelta(days=duration)

    try:
        ltp = kite.ltp([instrument])
        instrument_token = ltp[instrument]['instrument_token']
        candles = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval,
            continuous=False
        )
    except Exception as e:
        print(f"[Indicators] Error fetching data: {e}")
        return None, 0

    df = pd.DataFrame(candles)
    if df.empty or len(df) < 30:
        return None, 0

    df["HL2"] = (df["high"] + df["low"]) / 2
    df["OHLC4"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4

    # Moving Averages
    df["MA_3"] = df["OHLC4"].rolling(3).mean()
    df["MA_9"] = df["OHLC4"].rolling(9).mean()
    df["MA_20"] = df["OHLC4"].rolling(20).mean()
    df["MA_50"] = df["high"].ewm(span=50, adjust=False).mean()
    df["MA_200_WMA"] = df["high"].rolling(window=200).mean()

    # RSI (OHLC4)
    delta = df["OHLC4"].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    df["RSI_MA_9"] = df["RSI"].rolling(9).mean()
    df["RSI_MA_14"] = df["RSI"].rolling(14).mean()
    df["RSI_MA_26"] = df["RSI"].rolling(26).mean()

    # Price Volume
    df["PriceVolume"] = df["close"] * df["volume"]
    df["PV_MA"] = df["PriceVolume"].rolling(9).mean()

    # Linear Regression Slope (last 21 candles)
    def calc_lr_slope(series):
        x = np.arange(len(series))
        y = series.values
        if len(y) < 2:
            return 0
        slope, _ = np.polyfit(x, y, 1)
        return slope * 100  # scaled

    df["LR_Slope"] = df["high"].rolling(window=21).apply(calc_lr_slope, raw=False)

    latest = df.iloc[-1]
    above_mas = latest["close"] > max(
        latest["MA_3"], latest["MA_9"], latest["MA_20"], latest["MA_50"], latest["MA_200_WMA"]
    )
    rsi_strong = latest["RSI"] > max(latest["RSI_MA_9"], latest["RSI_MA_14"], latest["RSI_MA_26"])
    volume_spike = latest["PriceVolume"] > latest["PV_MA"] * 1.2
    slope_strong = latest["LR_Slope"] > 30

    # Direction Logic
    if above_mas and rsi_strong and slope_strong:
        direction = "CE"
    elif not above_mas and rsi_strong and slope_strong:
        direction = "PE"
    else:
        direction = None

    signal_strength = sum([above_mas, rsi_strong, volume_spike, slope_strong])
    return direction, signal_strength
