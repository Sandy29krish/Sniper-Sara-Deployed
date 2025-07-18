# utils/learning_engine.py

from datetime import datetime

# Learn from trade outcome and log internally
def learn_from_trade(symbol, direction, entry_price, exit_price, reason, strategy="expiry"):
    pnl = exit_price - entry_price if direction == "CE" else entry_price - exit_price
    result = "PROFIT" if pnl > 0 else "LOSS"
    
    print(f"[Learn] {symbol} | {strategy.upper()} | {result} | Entry: {entry_price}, Exit: {exit_price}, Reason: {reason}")
    # Placeholder: Save to ML model or pattern store in future
    return result

# Generate AI-style explanation for trade outcome (for stop-loss or mistake)
def learn_from_mistake(symbol, context, result="LOSS"):
    entry = context.get("entry_price")
    exit_ = context.get("exit_price")
    reason = context.get("reason")
    duration = context.get("duration", 0)

    insight = (
        f"Trade on {symbol} failed due to '{reason}'. Entry was {entry}, exit was {exit_}. "
        f"Held for {round(duration, 1)} minutes. Consider reevaluating signal strength, entry timing, or market volatility."
    )

    print(f"[AI Insight] {insight}")
    return insight
