import os
import telebot

# Load credentials from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validate presence of token and chat ID
if not BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not set in environment.")
    exit(1)

if not CHAT_ID:
    print("❌ TELEGRAM_CHAT_ID not set in environment.")
    exit(1)

try:
    bot = telebot.TeleBot(BOT_TOKEN)

    # Send a test message
    bot.send_message(chat_id=CHAT_ID, text="✅ Telegram test message sent successfully from Sniper bot!")

    print("✅ Telegram test message sent successfully.")

except Exception as e:
    print("❌ Telegram failed: A request to the Telegram API was unsuccessful.")
    print("Error:", e)
