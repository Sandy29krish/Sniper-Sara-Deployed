#!/bin/bash

echo "Starting Sniper expiry strategy bot..."

while true
do
  echo "Launching runner.py at $(date)"
  python3 runner.py
  echo "Restarting in 10 seconds after crash..."
  sleep 10
done
