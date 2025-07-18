#!/bin/bash

while true
do
  echo "🔁 Refreshing token and starting Sniper Bot..."

  # Refresh Zerodha access token
  python3 utils/auto_token_refresh.py

  # Export token to environment
  export KITE_ACCESS_TOKEN=$(cat access_token.txt)

  # Run main bot
  python3 runner.py

  echo "❌ Bot exited unexpectedly. Restarting in 60 seconds..."
  sleep 60
done
