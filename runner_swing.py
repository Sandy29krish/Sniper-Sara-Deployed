# runner_swing.py

import time
import threading
from strategy_swing import run_swing_strategy
from utils.telegram_commands import start_bot_listener, is_bot_active, get_bot_mode, send_telegram_message

def swing_loop():
    print("[Runner] Sniper Swing Strategy started.")
    while True:
        try:
            if is_bot_active():
                mode = get_bot_mode()
                print(f"[Runner Swing] Bot is ACTIVE | Mode: {mode}")
                run_swing_strategy()
            else:
                print("[Runner Swing] Bot is STOPPED. Waiting...")
            time.sleep(900)  # Run every 15 minutes for swing
        except Exception as e:
            print(f"[Runner Swing] Error in loop: {e}")
            time.sleep(900)

if __name__ == "__main__":
    # Start Telegram bot listener in background (shared for all bots)
    threading.Thread(target=start_bot_listener, daemon=True).start()
    time.sleep(5)  # Delay to let Telegram bot initialize

    try:
        send_telegram_message("✅ Sniper Swing Runner is LIVE and watching for swing setups.")
    except Exception as e:
        print(f"[Runner Swing] Telegram alert failed: {e}")

    swing_loop()
