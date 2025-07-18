# utils/ai_assistant.py

def explain_trade(symbol, direction, indicators):
    """
    Generate a human-readable reason for trade entry.
    """
    parts = []
    if indicators.get("above_200wma"):
        parts.append("Price is above all major MAs (incl. 200 WMA)")
    if indicators.get("rsi_strong"):
        parts.append("RSI is strong with upward momentum")
    if indicators.get("volume_spike"):
        parts.append("Volume surge indicates participation")
    if indicators.get("slope_strong"):
        parts.append("Price slope shows strong trend")
    
    if not parts:
        return f"{symbol} {direction} - Weak confirmation. Entry NOT advised."

    reason = " | ".join(parts)
    return f"{symbol} {direction} - Confirmed breakout setup: {reason}"


def should_enter_trade(conditions):
    """
    AI filtering logic — allows only strong signals.
    Rejects trades with signal strength < 4.
    """
    strength = conditions.get("signal_strength", 0)
    direction = conditions.get("direction")

    if not direction or strength < 4:
        return "NO - Weak signal, avoid entry"

    # Can expand this in future to check market-wide volatility, VIX, or news
    return "YES - Signal looks valid"


def learn_from_mistake(symbol, context, result="LOSS"):
    """
    Generates feedback based on failed trades.
    """
    entry = context.get("entry_price")
    exit_ = context.get("exit_price")
    reason = context.get("reason")
    duration = round(context.get("duration", 0), 1)

    insight = (
        f"{symbol} trade resulted in {result}. Reason: {reason}. "
        f"Entry at {entry}, exited at {exit_} after {duration} mins. "
        f"Review entry timing, signal confirmation, and option pricing."
    )

    return insight
