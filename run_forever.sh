#!/bin/bash
while true; do
  python runner.py
  echo "Sniper bot crashed with exit code $?. Restarting..." >&2
  sleep 5
done
