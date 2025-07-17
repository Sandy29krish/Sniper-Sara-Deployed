# Main runner for Sniper bot
import traceback
import time
from telegram_bot import TelegramBot
from strategy_expiry import run_expiry_strategy
from strategy_swing import run_swing_strategy

if __name__ == "__main__":
    try:
        print("🟢 Sniper bot is starting...")

        # Start Telegram command listener
        telegram_bot = TelegramBot()
        telegram_bot.start_command_listener()

        # Continuous loop to keep both strategies alive
        while True:
            run_expiry_strategy()
            run_swing_strategy()
            time.sleep(60)  # Adjust frequency as needed

    except Exception as e:
        print("❌ Fatal error:")
        traceback.print_exc()

