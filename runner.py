# Main runner for Sniper bot
import traceback
import time
from telegram_commands import start_bot_listener, is_bot_active, get_bot_mode, send_telegram_message
from strategy_expiry import run_expiry_strategy
from strategy_swing import run_swing_strategy

if __name__ == "__main__":
    try:
        print("🟢 Sniper bot is starting...")

        # Start Telegram command listener
        start_bot_listener()

        # Continuous loop to keep both strategies alive
        while True:
            if is_bot_active():
                mode = get_bot_mode()
                if mode == "LIVE":
                    run_expiry_strategy()
                    run_swing_strategy()
            time.sleep(60)  # Adjust frequency as needed

    except Exception as e:
        print("❌ Fatal error:")
        traceback.print_exc()
