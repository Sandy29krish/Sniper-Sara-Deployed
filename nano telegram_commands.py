import os
import telegram
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot_mode = {"mode": "STOPPED"}

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials not set.")
        return
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"[Telegram Error] {e}")

def start_bot_listener():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    def start(update, context):
        bot_mode["mode"] = "ACTIVE"
        context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Sniper Bot Started")

    def stop(update, context):
        bot_mode["mode"] = "STOPPED"
        context.bot.send_message(chat_id=update.effective_chat.id, text="🛑 Sniper Bot Stopped")

    def status(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"📊 Current Mode: {bot_mode['mode']}")

    dp.add_handler(CommandHandler("start_sniper", start))
    dp.add_handler(CommandHandler("stop_sniper", stop))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()

def is_bot_active():
    return bot_mode["mode"] == "ACTIVE"

def get_bot_mode():
    return bot_mode["mode"]
