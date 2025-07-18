# telegram_test.py
import telebot

BOT_TOKEN = "7582895487:AAF_LtUA1Beb1D91cVtr2qof9Z9PC9djYek"
CHAT_ID = "7582895487"  # Ensure it's a string

bot = telebot.TeleBot(BOT_TOKEN)

try:
    bot.send_message(CHAT_ID, "✅ Test message from Sniper Bot! Telegram is working.")
    print("✅ Message sent successfully.")
except Exception as e:
    print(f"❌ Telegram failed: {e}")
