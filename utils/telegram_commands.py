# utils/telegram_commands.py

import telebot
import os
import json

# Load from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your Telegram user ID or channel ID

# Initialize
bot = telebot.TeleBot(BOT_TOKEN)
STATUS = {"active": False, "mode": "IDLE"}

# Reusable alert function
def send_telegram_message(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"[Telegram Error] {e}")

# === Bot Commands ===
@bot.message_handler(commands=["start_sniper"])
def start_command(message):
    STATUS["active"] = True
    STATUS["mode"] = "LIVE"
    send_telegram_message("✅ Sniper bot started. Monitoring market...")

@bot.message_handler(commands=["stop_sniper"])
def stop_command(message):
    STATUS["active"] = False
    STATUS["mode"] = "STOPPED"
    send_telegram_message("🛑 Sniper bot stopped.")

@bot.message_handler(commands=["status"])
def status_command(message):
    msg = f"🤖 Bot Status: {'✅ ACTIVE' if STATUS['active'] else '⛔ STOPPED'}\nMode: {STATUS['mode']}"
    send_telegram_message(msg)

@bot.message_handler(commands=["pnl"])
def pnl_command(message):
    try:
        with open("trade_log.json", "r") as f:
            data = json.load(f)
            msg = f"📊 Trades:\n{json.dumps(data, indent=2)}"
            send_telegram_message(msg)
    except:
        send_telegram_message("⚠️ No trade log found or unable to read it.")

# === External call support ===
def start_bot_listener():
    print("[Telegram] Bot listener started.")
    bot.polling(none_stop=True)

def is_bot_active():
    return STATUS["active"]

def get_bot_mode():
    return STATUS["mode"]
