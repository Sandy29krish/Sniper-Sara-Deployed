import numpy as np
import pandas as pd
import yfinance as yf

def calculate_indicators(symbol, timeframe="1minute", mode="expiry"):
    """
    Fetch live/historical data and calculate 4-step signal confirmation:
    1. Price above all MAs including 200 WMA
    2. RSI > RSI MAs
    3. Price volume increasing
    4. LR slope > 30
    Returns: direction ("CALL"/"PUT") and signal strength (0 to 4)
    """
    try:
        df = fetch_recent_data(symbol, timeframe)

        if df is None or len(df) < 200:
            return None, 0

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        # === STEP 1: Price > All MAs ===
        price = latest['close']
        ma_3 = df['ma_3'].iloc[-1]
        ma_9 = df['ma_9'].iloc[-1]
        ma_20 = df['ma_20'].iloc[-1]
        ma_50 = df['ma_50'].iloc[-1]
        ma_200 = df['ma_200'].iloc[-1]

        price_condition = price > ma_3 > ma_9 > ma_20 > ma_50 > ma_200

        # === STEP 2: RSI > RSI MA ===
        rsi = latest['rsi']
        rsi_ma_9 = df['rsi_ma_9'].iloc[-1]
        rsi_ma_14 = df['rsi_ma_14'].iloc[-1]

        rsi_condition = rsi > rsi_ma_9 > rsi_ma_14

        # === STEP 3: Price volume condition ===
        volume_strength = (latest['close'] - prev['close']) * latest['volume']
        price_vol_condition = volume_strength > df['volume'].mean() * 1.2

        # === STEP 4: LR Slope > 30 ===
        lr_slope = df['lr_slope'].iloc[-1]
        slope_condition = lr_slope > 30

        # === Combine ===
        signal_strength = sum([price_condition, rsi_condition, price_vol_condition, slope_condition])

        if signal_strength >= 3:
            direction = "CALL" if price > prev['close'] else "PUT"
            return direction, signal_strength

        return None, signal_strength

    except Exception as e:
        print(f"[Indicators] Error: {e}")
        return None, 0


def fetch_recent_data(symbol, timeframe):
    """
    Placeholder: Replace with live OHLC data fetch via Zerodha/Kite
    """
    interval = "1m" if timeframe == "1minute" else "3m"
    df = yf.download(tickers=f"{symbol}.NS", period="5d", interval=interval, progress=False)

    if df.empty:
        return None

    df.rename(columns={
        "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"
    }, inplace=True)

    # === Indicators ===
    df['ma_3'] = df['close'].rolling(3).mean()
    df['ma_9'] = df['close'].rolling(9).mean()
    df['ma_20'] = df['close'].rolling(20).mean()
    df['ma_50'] = df['close'].rolling(50).mean()
    df['ma_200'] = df['close'].rolling(200).mean()

    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(21).mean()
    avg_loss = pd.Series(loss).rolling(21).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df['rsi'] = 100 - (100 / (1 + rs))
    df['rsi_ma_9'] = df['rsi'].rolling(9).mean()
    df['rsi_ma_14'] = df['rsi'].rolling(14).mean()

    df['lr_slope'] = df['high'].rolling(21).apply(linear_regression_slope, raw=True)

    return df


def linear_regression_slope(series):
    y = np.array(series)
    x = np.arange(len(y))
    if len(y) < 2:
        return 0
    A = np.vstack([x, np.ones(len(x))]).T
    m, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    return m * 100  # Convert to scaled value
