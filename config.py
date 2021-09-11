import os

# CoinMarketCap Pro API key
CMC_API_KEY = os.getenv("CMC_TOKEN")

# The token of the @Replit_Bitcoin_Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# The chat ID to send message and bypass python-telegram-bot send message limitation
CHAT_ID = os.getenv("CHAT_TOKEN")

# Do APIs requests at 60 minutes time interval
TIME_INTERVAL = 60 * 60 

# Market symbol to pull from CoinMarketCap
MARKET_SYMBOL = 'BTC'

# Currency ISO to pull from CoinMarketCap
CURRENCY_ISO = 'USD'

# Percentage thresholds to notify user (5%)
LOWER_THRESHOLD = -5  
UPPER_THRESHOLD = 5