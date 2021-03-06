import os

# CoinMarketCap Pro API key
CMC_API_KEY = os.getenv("CMC_TOKEN")

# The token of the @Replit_Bitcoin_Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Do API requests at 60 minutes time interval
TIME_INTERVAL = 60 * 60

# Market symbol to pull from CoinMarketCap
MARKET_SYMBOL = 'BTC'

# Currency ISO to pull from CoinMarketCap
CURRENCY_ISO = 'USD'

# Set locale for formatting numbers and text
LOCALE = "en_US.UTF-8"

# Percentage thresholds to notify users (5%)
LOWER_THRESHOLD = -5  
UPPER_THRESHOLD = 5