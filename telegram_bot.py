# telegram_bot.py

import telebot
import os

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = telebot.TeleBot(self.token)
        self.mode = "STOPPED"

        @self.bot.message_handler(commands=["start_sniper"])
        def start_command(message):
            self.mode = "ACTIVE"
            self.bot.reply_to(message, "✅ Sniper bot started.")
        
        @self.bot.message_handler(commands=["stop_sniper"])
        def stop_command(message):
            self.mode = "STOPPED"
            self.bot.reply_to(message, "🛑 Sniper bot stopped.")

        @self.bot.message_handler(commands=["status"])
        def status_command(message):
            self.bot.reply_to(message, f"📡 Current bot status: {self.mode}")

        @self.bot.message_handler(commands=["pnl"])
        def pnl_command(message):
            try:
                from trade_logger import get_today_summary
                summary = get_today_summary()
                self.bot.reply_to(message, summary)
            except Exception as e:
                self.bot.reply_to(message, f"⚠️ Error fetching PnL: {e}")

    def send_message(self, msg):
        try:
            self.bot.send_message(self.chat_id, msg)
        except Exception as e:
            print(f"[TelegramBot] Failed to send message: {e}")

    def run(self):
        self.bot.polling(non_stop=True)

    def is_active(self):
        return self.mode == "ACTIVE"
