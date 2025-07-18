import telebot
import os
import json

# Load from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Telegram User or Channel ID

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Global bot status
STATUS = {"active": False, "mode": "IDLE"}

# === Utility: Telegram Message Sender ===
def send_telegram_message(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"[Telegram Error] {e}")

# === Command Handlers ===
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
    status_msg = (
        f"🤖 Bot Status: {'✅ ACTIVE' if STATUS['active'] else '⛔ STOPPED'}\n"
        f"Mode: {STATUS['mode']}"
    )
    send_telegram_message(status_msg)

@bot.message_handler(commands=["pnl"])
def pnl_command(message):
    try:
        with open("trade_log.json", "r") as f:
            data = json.load(f)
        formatted = json.dumps(data, indent=2)
        send_telegram_message(f"📊 Trades:\n{formatted}")
    except Exception as e:
        send_telegram_message(f"⚠️ Error reading trade log: {e}")

# === Start Listener ===
def start_bot_listener():
    print("[Telegram] Bot listener started.")
    bot.polling(none_stop=True)

# === Status Accessors for Runner ===
def is_bot_active():
    return STATUS["active"]

def get_bot_mode():
    return STATUS["mode"]
