import os
import telebot

# Fetch from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Must be numeric string (like: "7582895487")

# Validate token and chat ID
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment.")
    exit(1)

# Create bot instance
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

try:
    # Send test message
    bot.send_message(TELEGRAM_CHAT_ID, "✅ Telegram bot is working correctly!")
    print("✅ Telegram test message sent successfully.")
except Exception as e:
    print(f"❌ Telegram failed: {e}")
