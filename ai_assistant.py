# utils/ai_assistant.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_trade(symbol, direction, indicators):
    try:
        prompt = (
            f"A trade is being planned on {symbol} with a {direction} direction.\n"
            f"Indicators: {indicators}\n"
            f"Explain why this trade is valid."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"AI explanation error: {e}"

def learn_from_mistake(symbol, context, result="LOSS"):
    try:
        prompt = (
            f"The trade on {symbol} resulted in a {result}.\n"
            f"Context: {context}\n"
            f"What can we learn from this failure?"
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Learning error: {e}"

def should_enter_trade(context):
    try:
        prompt = (
            f"Given the current market signal:\n"
            f"{context}\n"
            f"Should we enter this trade? Reply YES or NO with a short reason."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return "NO - AI decision failed"
