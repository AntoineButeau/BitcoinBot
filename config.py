import os

# CoinMarketCap Pro API key
CMC_API_KEY = os.getenv("CMC_TOKEN")

# The token of the @Replit_Bitcoin_Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# The chat ID to send message
CHAT_ID = os.getenv("CHAT_TOKEN")

# Do APIs requests with pause
TIME_INTERVAL = 30 * 60  # in seconds, 30 minutes time interval

# Market symbol to pull from CoinMarketCap
MARKET_SYMBOL = 'BTC'

# Currency ISO to pull from CoinMarketCap
CURRENCY_ISO = 'USD'

# Thresholds to notify user
LOWER_THRESHOLD = 45600  # Bitcoin lower price threshold - TODO, need to take into account currency and latest price, probably also doesnt fit the use case I'm trying to achieve, so need to take into account historical price somewhat
UPPER_THRESHOLD = 46000  # Bitcoin upper threshold