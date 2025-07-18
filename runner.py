# runner.py

import time
import threading
from strategy_expiry import run_expiry_strategy
from utils.telegram_commands import start_bot_listener, is_bot_active, get_bot_mode, send_telegram_message

def main_loop():
    print("[Runner] Sniper strategy monitor started.")
    while True:
        try:
            if is_bot_active():
                mode = get_bot_mode()
                print(f"[Runner] Bot is ACTIVE | Mode: {mode}")
                run_expiry_strategy()
            else:
                print("[Runner] Bot is STOPPED. Waiting...")
            time.sleep(60)  # Check every 1 minute
        except Exception as e:
            print(f"[Runner] Error in main loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Start Telegram bot listener in background
    threading.Thread(target=start_bot_listener, daemon=True).start()
    time.sleep(5)  # small delay to stabilize listener

    try:
        send_telegram_message("✅ Sniper Runner is LIVE and ready.")
    except Exception as e:
        print(f"[Runner] Telegram alert failed: {e}")

    main_loop()
from utils.ai_assistant import explain_trade
from utils.telegram_commands import send_telegram_message

# Send startup message
send_telegram_message("🤖 Sniper Bot Runner has started.")

# Add an AI explanation for context
reason = explain_trade("BANKNIFTY", "CE", {
    "above_200wma": True,
    "rsi_strong": True,
    "volume_spike": True,
    "slope_strong": True,
    "strength": 4
})
send_telegram_message(f"🧠 AI Trade Setup Context:\n{reason}")
