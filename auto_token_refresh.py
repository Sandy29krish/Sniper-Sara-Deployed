# auto_token_refresher.py

import os
import pyotp
import requests
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect

def generate_totp():
    totp_secret = os.getenv("TOTP_SECRET")
    return pyotp.TOTP(totp_secret).now()

def auto_login_and_get_token():
    kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

    user_id = os.getenv("KITE_USER_ID")
    password = os.getenv("KITE_PASSWORD")
    totp = generate_totp()

    session = requests.Session()

    try:
        # Step 1: Get login page
        login_url = "https://kite.zerodha.com/api/login"
        session.get(login_url)

        # Step 2: Submit login
        login_payload = {
            "user_id": user_id,
            "password": password
        }
        response = session.post("https://kite.zerodha.com/api/login", data=login_payload)
        response.raise_for_status()

        # Step 3: Submit 2FA (TOTP)
        twofa_payload = {
            "user_id": user_id,
            "request_id": response.json()["data"]["request_id"],
            "twofa_value": totp,
            "twofa_type": "totp"
        }
        twofa_response = session.post("https://kite.zerodha.com/api/twofa", data=twofa_payload)
        twofa_response.raise_for_status()

        # Step 4: Get request token
        redirect_url = twofa_response.json()["data"]["redirect_url"]
        request_token = parse_qs(urlparse(redirect_url).query)["request_token"][0]

        # Step 5: Get access token
        data = kite.generate_session(request_token, api_secret=os.getenv("KITE_API_SECRET"))
        access_token = data["access_token"]

        # Save access token to .env or file
        with open("access_token.txt", "w") as f:
            f.write(access_token)

        return access_token

    except Exception as e:
        print("❌ Auto token refresh failed:", str(e))
        return None

