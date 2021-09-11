import os

# CoinMarketCap Pro API key
CMC_API_KEY = os.getenv("CMC_TOKEN")

# The token of the @Replit_Bitcoin_Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# The chat ID to send message
CHAT_ID = os.getenv("CHAT_TOKEN")

# Do APIs requests with pause
TIME_INTERVAL = 60 * 60  # in seconds, 60 minutes time interval

# Market symbol to pull from CoinMarketCap
MARKET_SYMBOL = 'BTC'

# Currency ISO to pull from CoinMarketCap
CURRENCY_ISO = 'USD'

# Thresholds to notify user
LOWER_THRESHOLD = -5  
UPPER_THRESHOLD = 5