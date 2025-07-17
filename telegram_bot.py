import os
import telebot

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)

    def start_command_listener(self):
        @self.bot.message_handler(commands=['start_sniper'])
        def start_sniper(message):
            self.send_message("🟢 Sniper bot started!")
            os.environ["BOT_STATUS"] = "ACTIVE"

        @self.bot.message_handler(commands=['stop_sniper'])
        def stop_sniper(message):
            self.send_message("🔴 Sniper bot stopped!")
            os.environ["BOT_STATUS"] = "STOPPED"

        @self.bot.message_handler(commands=['status'])
        def status(message):
            current_status = os.getenv("BOT_STATUS", "UNKNOWN")
            self.send_message(f"📊 Current bot status: {current_status}")

        self.bot.polling()
