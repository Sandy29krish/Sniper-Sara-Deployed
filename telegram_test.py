import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

message = "✅ Test message from Sniper bot!"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})

if response.status_code == 200:
    print("✅ Message sent successfully")
else:
    print(f"❌ Telegram failed: {response.status_code} - {response.text}")
