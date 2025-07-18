from kiteconnect import KiteConnect
import os

kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
kite.set_access_token(os.getenv("KITE_ACCESS_TOKEN"))
