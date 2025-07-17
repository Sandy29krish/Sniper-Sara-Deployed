# auto_token_refresher.py

import pyotp
import requests
from urllib.parse import parse_qs, urlparse
import os

def generate_totp():
    secret = os.getenv("ZERODHA_TOTP_SECRET")
    totp = pyotp.TOTP(secret)
    return totp.now()

def auto_login():
    try:
        user_id = os.getenv("ZERODHA_USER_ID")
        password = os.getenv("ZERODHA_PASSWORD")
        twofa = generate_totp()

        # Zerodha login step
        session = requests.Session()
        login_resp = session.post("https://kite.zerodha.com/api/login", data={
            "user_id": user_id,
            "password": password
        })

        if login_resp.status_code != 200:
            raise Exception("Login request failed")

        # Two-factor authentication step
        twofa_resp = session.post("https://kite.zerodha.com/api/twofa", data={
            "user_id": user_id,
            "request_id": login_resp.json().get("data", {}).get("request_id"),
            "twofa_value": twofa
        })

        if twofa_resp.status_code != 200:
            raise Exception("2FA failed")

        # Get request_token from redirected URL
        redirect_url = twofa_resp.json().get("data", {}).get("redirect_url")
        if not redirect_url:
            raise Exception("No redirect URL after login")

        parsed_url = urlparse(redirect_url)
        request_token = parse_qs(parsed_url.query)["request_token"][0]

        # Exchange request_token for access_token
        api_key = os.getenv("ZERODHA_API_KEY")
        api_secret = os.getenv("ZERODHA_API_SECRET")
        access_token_resp = requests.post("https://api.kite.trade/session/token", data={
            "api_key": api_key,
            "request_token": request_token,
            "checksum": generate_checksum(api_key, request_token, api_secret)
        })

        access_token = access_token_resp.json()["data"]["access_token"]
        with open("access_token.txt", "w") as f:
            f.write(access_token)
        print("[Auto Login] Access token refreshed successfully.")
        return access_token

    except Exception as e:
        print(f"[Auto Login] Failed to auto-login: {e}")
        return None

def generate_checksum(api_key, request_token, api_secret):
    import hashlib
    import hmac
    payload = f"{api_key}{request_token}{api_secret}"
    return hmac.new(api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


---

✅ Environment Variables Required:

Variable	Description

ZERODHA_USER_ID	Your Kite ID
ZERODHA_PASSWORD	Your Kite password
ZERODHA_TOTP_SECRET	TOTP secret (App code setup key)
ZERODHA_API_KEY	Zerodha API key
ZERODHA_API_SECRET	Zerodha API secret



---

🔐 Access Token Location:

Saved to access_token.txt for re-use by kite_connect = KiteConnect(...)



---

Shall I proceed to learning_engine.py, captain? 🧠

