# utils/sniper_historical_backtest.py

import yfinance as yf
import pandas as pd
from utils.indicators import calculate_indicators
from utils.lot_manager import calculate_lot_size
from utils.nse_data import get_expiry_date
from datetime import timedelta

CAPITAL = 200000  # change as needed
PREMIUM_ENTRY = 30  # simulated OTM premium price
TAKE_PROFIT_1 = 1.85
TAKE_PROFIT_2 = 2.1
STOP_LOSS_FACTOR = 0.65  # 35% SL

def run_comprehensive_backtest(symbol: str, from_date: str, to_date: str):
    df = yf.download(symbol, start=from_date, end=to_date, interval="1m")
    df.dropna(inplace=True)
    df['Datetime'] = df.index

    trades = []
    in_trade = False
    entry_price = 0
    entry_time = None
    trade_side = None
    lot_size = calculate_lot_size(CAPITAL, PREMIUM_ENTRY)

    for i in range(len(df)):
        current = df.iloc[i]
        ts = current.name

        if not in_trade:
            direction, strength = calculate_indicators(df.iloc[:i+1], symbol, timeframe="1minute", mode="expiry", historical=True)
            if direction and strength >= 3:
                in_trade = True
                entry_price = PREMIUM_ENTRY
                entry_time = ts
                trade_side = direction
                trades.append({
                    'type': direction,
                    'entry_time': ts,
                    'entry_price': PREMIUM_ENTRY,
                    'exit_price': None,
                    'exit_time': None,
                    'pnl': None
                })
        else:
            # Simulate option premium price
            simulated_price = PREMIUM_ENTRY * ((1 + (i % 10) * 0.01))
            take_profit_1 = PREMIUM_ENTRY * TAKE_PROFIT_1
            take_profit_2 = PREMIUM_ENTRY * TAKE_PROFIT_2
            stop_loss = PREMIUM_ENTRY * STOP_LOSS_FACTOR

            if simulated_price >= take_profit_1:
                exit_price = take_profit_1
                trades[-1]['exit_time'] = ts
                trades[-1]['exit_price'] = exit_price
                trades[-1]['pnl'] = round((exit_price - entry_price) * lot_size, 2)
                in_trade = False

            elif simulated_price <= stop_loss or ts.hour == 15 and ts.minute >= 14:
                exit_price = simulated_price
                trades[-1]['exit_time'] = ts
                trades[-1]['exit_price'] = exit_price
                trades[-1]['pnl'] = round((exit_price - entry_price) * lot_size, 2)
                in_trade = False

    df_trades = pd.DataFrame(trades)
    total_pnl = df_trades['pnl'].sum()
    print(f"\n🔁 Backtest Summary for {symbol} from {from_date} to {to_date}")
    print(df_trades[['entry_time', 'exit_time', 'entry_price', 'exit_price', 'type', 'pnl']])
    print(f"\n📊 Total PnL: ₹{total_pnl:.2f} over {len(df_trades)} trades")

    return df_trades
