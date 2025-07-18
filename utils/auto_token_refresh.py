import os
import time
import pyotp
import requests
from kiteconnect import KiteConnect

def generate_totp(secret):
    return pyotp.TOTP(secret).now()

def auto_login_and_get_token():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys

        kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
        user_id = os.getenv("USER_ID")
        password = os.getenv("PASSWORD")
        totp_secret = os.getenv("TOTP_SECRET")

        totp = generate_totp(totp_secret)
        login_url = kite.login_url()

        # Headless Chrome setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(login_url)

        # Fill login
        driver.find_element(By.ID, "userid").send_keys(user_id)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Enter TOTP
        driver.find_element(By.TAG_NAME, "input").send_keys(totp)
        driver.find_element(By.XPATH, "//button").click()
        time.sleep(2)

        # Get request_token from redirect URL
        current_url = driver.current_url
        request_token = current_url.split("request_token=")[1].split("&")[0]
        driver.quit()

        # Generate access token
        data = kite.generate_session(request_token, api_secret=os.getenv("KITE_API_SECRET"))
        access_token = data["access_token"]

        # Save to file or environment
        with open("access_token.txt", "w") as f:
            f.write(access_token)

        print("[Auto Login] Access token refreshed successfully.")
        return access_token

    except Exception as e:
        print(f"[Auto Login] Failed: {e}")
        return None
