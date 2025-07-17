#!/bin/bash
# This script keeps restarting the Sniper bot every 10 seconds if it stops

while true
do
  echo "[SNIPER BOT] Running..."
  python3 runner.py
  echo "[SNIPER BOT] Crashed or stopped. Restarting in 10 seconds..."
  sleep 10
done
