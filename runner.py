# runner.py

import time
from strategy_expiry import run_expiry_strategy
from telegram_commands import start_bot_listener, is_bot_active, get_bot_mode
import threading

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
    threading.Thread(target=start_bot_listener).start()
    time.sleep(5)  # small delay to stabilize listener
    main_loop()
