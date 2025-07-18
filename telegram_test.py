# telegram_test.py

from settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import telebot

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

try:
    bot.send_message(TELEGRAM_CHAT_ID, "✅ Test message from Sniper bot is working!")
    print("✅ Telegram message sent.")
except Exception as e:
    print(f"❌ Telegram failed: {e}")
