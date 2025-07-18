import openai import os import json

openai.api_key = os.getenv("OPENAI_API_KEY")

====== AI Trade Insight Generator ======

def explain_trade(symbol, direction, indicators): prompt = f""" You are an expert trading assistant. Explain the reasoning behind entering a trade.

Symbol: {symbol} Direction: {direction} Indicators:

Above 200 WMA: {indicators.get('above_200wma')}

RSI > MA: {indicators.get('rsi_strong')}

Price Volume Surge: {indicators.get('volume_spike')}

LR Slope > 30: {indicators.get('slope_strong')}

Signal Strength: {indicators.get('strength')}/4


Write a concise explanation with 2–3 lines suitable for Telegram. """ try: response = openai.ChatCompletion.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a concise and smart trading assistant."}, {"role": "user", "content": prompt} ], max_tokens=120 ) return response.choices[0].message.content.strip() except Exception as e: print(f"[AI Error - explain_trade] {e}") return "AI explanation unavailable."

====== AI Fallback Decision ======

def fallback_decision(reason): prompt = f""" NSE data fetch failed due to: {reason} Suggest what the bot should do today. Return a 1-line decision. """ try: response = openai.ChatCompletion.create( model="gpt-4", messages=[ {"role": "system", "content": "You help a trading bot make safe fallback decisions."}, {"role": "user", "content": prompt} ], max_tokens=60 ) return response.choices[0].message.content.strip() except Exception as e: print(f"[AI Error - fallback_decision] {e}") return "Skip today's trade due to technical error."

====== AI Summary of PnL ======

def summarize_pnl(trade_log): prompt = f""" Analyze the following trade history and give a 3-line summary with key insights: {json.dumps(trade_log[-10:], indent=2)} """ try: response = openai.ChatCompletion.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a trading strategist analyzing PnL data."}, {"role": "user", "content": prompt} ], max_tokens=150 ) return response.choices[0].message.content.strip() except Exception as e: print(f"[AI Error - summarize_pnl] {e}") return "Unable to generate summary."

====== Learn from Losses ======

def learn_from_mistake(symbol, context, result): prompt = f""" Analyze this failed trade for learning: Symbol: {symbol} Result: {result} Context: {json.dumps(context, indent=2)}

Give 2 lines of insight to improve future trades. """ try: response = openai.ChatCompletion.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a trading AI that learns from failed setups."}, {"role": "user", "content": prompt} ], max_tokens=100 ) return response.choices[0].message.content.strip() except Exception as e: print(f"[AI Error - learn_from_mistake] {e}") return "Learning insight not available."

====== AI Entry Sanity Check ======

def should_enter_trade(current_conditions): prompt = f""" Given the following market conditions, should we enter the trade?

Conditions: {json.dumps(current_conditions, indent=2)}

Reply YES or NO with 1-line reason. """ try: response = openai.ChatCompletion.create( model="gpt-4", messages=[ {"role": "system", "content": "You help approve only high-quality trades."}, {"role": "user", "content": prompt} ], max_tokens=50 ) return response.choices[0].message.content.strip() except Exception as e: print(f"[AI Error - should_enter_trade] {e}") return "NO – Error checking setup."

