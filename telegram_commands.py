telegram_commands.py

import telebot
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") 
# Your Telegram user ID or channel ID

bot = telebot.TeleBot(BOT_TOKEN)

STATUS = {"active": False, "mode": "IDLE"}  # Global bot control

def send_telegram_message(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"[Telegram Error] {e}")
# ======================== Command Handlers ========================
@bot.message_handler(commands=["start_sniper"]) 
def start_command(message): 
    STATUS["active"] = True 
    STATUS["mode"] = "LIVE" 
    send_telegram_message("✅ Sniper bot started. Monitoring live market conditions...")

@bot.message_handler(commands=["stop_sniper"]) 
def stop_command(message): 
    STATUS["active"] = False 
    STATUS["mode"] = "STOPPED" 
    send_telegram_message("🛑 Sniper bot stopped by user.")

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
            send_telegram_message(f"📊 Trades:\n{json.dumps(data, indent=2)}")
    except:
        send_telegram_message("⚠️ No trade log found or error reading the file.")
def start_bot_listener():
    print("[Telegram] Bot listener started.")
    bot.polling(none_stop=True)

def is_bot_active():
    return STATUS["active"]

def get_bot_mode():
    return STATUS["mode"]
    # Optional: to auto-start in dev environment
if __name__ == "__main__":
    start_bot_listener()
