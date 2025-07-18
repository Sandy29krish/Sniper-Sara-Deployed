import telebot import os import json 
from utils.ai_assistant import explain_trade, get_trade_summary, learn_from_mistake

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

STATUS = {"active": False, "mode": "IDLE"}  # Global bot control

def send_telegram_message(message): try: bot.send_message(CHAT_ID, message) except Exception as e: print(f"[Telegram Error] {e}")

======================== Command Handlers ========================

@bot.message_handler(commands=["start_sniper"]) def start_command(message): STATUS["active"] = True STATUS["mode"] = "LIVE" send_telegram_message("✅ Sniper bot started. Monitoring live market conditions...")

@bot.message_handler(commands=["stop_sniper"]) def stop_command(message): STATUS["active"] = False STATUS["mode"] = "STOPPED" send_telegram_message("🛑 Sniper bot stopped by user.")

@bot.message_handler(commands=["status"]) def status_command(message): status_msg = ( f"🤖 Bot Status: {'✅ ACTIVE' if STATUS['active'] else '⛔ STOPPED'}\n" f"Mode: {STATUS['mode']}" ) send_telegram_message(status_msg)

@bot.message_handler(commands=["pnl"]) def pnl_command(message): try: with open("trade_log.json", "r") as f: data = json.load(f) send_telegram_message(f"📊 Trades:\n{json.dumps(data, indent=2)}") except: send_telegram_message("⚠️ No trade log found or error reading the file.")

@bot.message_handler(commands=["why"]) def why_command(message): dummy_indicators = { "above_200wma": True, "rsi_strong": True, "volume_spike": True, "slope_strong": True, "strength": 4 } reason = explain_trade("BANKNIFTY", "CALL", dummy_indicators) send_telegram_message(f"🧠 Reason for entry: {reason}")

@bot.message_handler(commands=["ai_summary"]) def ai_summary_command(message): try: with open("trade_log.json", "r") as f: data = json.load(f) summary = get_trade_summary(data) send_telegram_message(f"📈 AI Summary:\n{summary}") except: send_telegram_message("⚠️ No trade log found to summarize.")

@bot.message_handler(commands=["fail_reason"]) def fail_reason_command(message): sample_context = { "entry_price": 50, "exit_price": 30, "reason": "Stop Loss Hit", "duration": 10 } insight = learn_from_mistake("NIFTY", sample_context, result="LOSS") send_telegram_message(f"📉 Learning from Mistake:\n{insight}")

def start_bot_listener(): print("[Telegram] Bot listener started.") bot.polling(none_stop=True)

def is_bot_active(): return STATUS["active"]

def get_bot_mode(): return STATUS["mode"]

if name == "main": start_bot_listener()

