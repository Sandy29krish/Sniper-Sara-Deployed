#!/bin/bash
export PYTHONPATH=$(pwd)
while true
do
  echo "🔁 Restarting Sniper bot..."
  python3 runner.py
  sleep 5
done
