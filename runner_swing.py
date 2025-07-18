import time
import threading
from strategy_swing import run_swing_strategy
from utils.telegram_commands import start_bot_listener, is_bot_active, get_bot_mode, send_telegram_message

def main_loop():
    print("[Swing Runner] Sniper swing monitor started.")
    while True:
        try:
            if is_bot_active():
                mode = get_bot_mode()
                print(f"[Swing Runner] Bot is ACTIVE | Mode: {mode}")
                run_swing_strategy()
            else:
                print("[Swing Runner] Bot is STOPPED. Waiting...")
            time.sleep(900)  # Check every 15 minutes
        except Exception as e:
            print(f"[Swing Runner] Error in main loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=start_bot_listener, daemon=True).start()
    time.sleep(5)
    try:
        send_telegram_message("✅ Sniper Swing Runner is LIVE and ready.")
    except Exception as e:
        print(f"[Swing Runner] Telegram alert failed: {e}")
    main_loop()
