telegram_bot.py

import telebot import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your Telegram user ID or channel ID

bot = telebot.TeleBot(BOT_TOKEN)

STATUS = {"active": False, "mode": "IDLE"}  # Global bot control

def send_telegram_message(message): try: bot.send_message(CHAT_ID, message) except Exception as e: print(f"[Telegram] Failed to send message: {e}")

========================= Command Handlers =============================

@bot.message_handler(commands=["start_sniper"]) def start_command(message): STATUS["active"] = True STATUS["mode"] = "LIVE" send_telegram_message("✅ Sniper bot started. Monitoring live market conditions...")

@bot.message_handler(commands=["stop_sniper"]) def stop_command(message): STATUS["active"] = False STATUS["mode"] = "STOPPED" send_telegram_message("🛑 Sniper bot stopped by user.")

@bot.message_handler(commands=["status"]) def status_command(message): status_msg = f"🤖 Bot Status
