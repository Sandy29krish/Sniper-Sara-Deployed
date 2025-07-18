# ai_assistant.py

def explain_trade(symbol, direction, indicators):
    parts = []
    if indicators.get("above_200wma"):
        parts.append("above 200 WMA")
    if indicators.get("rsi_strong"):
        parts.append("strong RSI")
    if indicators.get("volume_spike"):
        parts.append("volume spike")
    if indicators.get("slope_strong"):
        parts.append("strong trend slope")
    if not parts:
        return f"{symbol} {direction} — no strong signals"
    return f"{symbol} {direction} — signals: {', '.join(parts)}"

def should_enter_trade(current_conditions):
    return "YES" if current_conditions.get("signal_strength", 0) >= 4 else "NO"

def learn_from_mistake(symbol, context, result="LOSS"):
    return (
        f"{symbol} trade {result}. Reason: {context.get('reason')}. "
        f"Entry at {context.get('entry_price')}, exit at {context.get('exit_price')}. "
        f"Duration: {round(context.get('duration',0),1)} min."
    )
