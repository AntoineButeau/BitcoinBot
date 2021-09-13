import config
import requests
import time
import logging
import locale
from emoji import emojize

# Set locale for formatting separators
locale.setlocale(locale.LC_ALL, config.LOCALE)

# Dictionary to fill/update when people interact with the bot for the first time. Somewhat hackish for now, probably better to use the Repl database
mybots = {}

# Start function to handle /start command
def start_command(update, context):
    update.message.reply_text("Hello there! This bot checks the BTC price every hour and sends alerts if it drops or rises by more than 5%")
    
    #Get user chat id and add related bot
    mybots[update.message.chat_id] = context.bot

# Help function to handle /help command
def help_command(update, context):
    update.message.reply_text("This bot doesn't do much else yet. Try /price to get latest BTC market information or /satoshi to get a link to the Bitcoin whitepaper")

# Satoshi Whitepaper function to handle /satoshi and send 
def satoshi_whitepaper_command(update, context):
    update.message.reply_text(text="<a href='https://bitcoin.org/bitcoin.pdf'>Satoshi Whitepaper</a>",parse_mode="HTML")

# Price function to handle /price command and send CoinMarketCap BTC information
def price_command(update, context):
    update.message.reply_text(get_btc_market_information())

# Function to set and format BTC market information to users
def get_btc_market_information():

    btc_data_dict = fetch_data_from_coinmarketcap_api()
    
    # Get BTC price
    btc_price = "$" + str(locale.format("%.2f", float(btc_data_dict["price"]), True))

    # Get 1 hour price change with emoji
    rate1h_float = btc_data_dict["percent_change_1h"]
    rate1h_emoji = parse_price_change(rate1h_float)
    rate1h = locale.format("%.2f", rate1h_float, True)

    # Get 24 hour price change with emoji
    rate24h_float = btc_data_dict["percent_change_24h"]
    rate24h_emoji = parse_price_change(rate24h_float)
    rate24h = locale.format("%.2f", rate24h_float, True)

    # Get 7 days price change with emoji
    rate7d_float = btc_data_dict["percent_change_7d"]
    rate7d_emoji = parse_price_change(rate7d_float)
    rate7d = locale.format("%.2f", rate7d_float, True)

    # Get BTC marketcap dominance
    btc_dominance = str(locale.format("%.2f", float(btc_data_dict["market_cap_dominance"]), True)) + "%"

    # Get BTC marketcap 
    btc_market_cap = "$" + str(locale.format("%.2f", float(btc_data_dict["market_cap"]), True))

    # Format message for users
    msg_market_information = "\nPrice: " + btc_price \
                                 + "\nLast 1 hour change: " + rate1h + "%" + rate1h_emoji \
                                 + "\nLast 24 hours change: " + rate24h + "%" + rate24h_emoji \
                                 + "\nLast 7 days change: " + rate7d + "%" + rate7d_emoji \
                                 + "\nBTC dominance: " + btc_dominance \
                                 + "\nMarket Cap: " + btc_market_cap + "\n"

    return msg_market_information

# Function to get the percentage of change vs. threshold and send message if needed
def get_price_percentage_change_against_threshold():
    while True:

        # Get 1h percentage of change
        btc_data_dict = fetch_data_from_coinmarketcap_api()
        rate1h_float = btc_data_dict["percent_change_1h"]

        # If the percentage of change falls below threshold, send an immediate msg
        if rate1h_float <= config.LOWER_THRESHOLD:
            rate1h_emoji = parse_price_change(rate1h_float)
            rate1h_msg = str(locale.format("%.2f", rate1h_float, True))
        
            btc_price_msg = "$" + str(locale.format("%.2f", float(btc_data_dict["price"]), True))

            msg_threshold = "\nBTC price drop alert: " + rate1h_msg + "%" + rate1h_emoji \
                            + "\nBTC price now at: " + btc_price_msg + "\n"

            send_message(msg=msg_threshold)

        # If the percentage of change rises above threshold, send an immediate msg
        if rate1h_float >= config.UPPER_THRESHOLD:
            rate1h_emoji = parse_price_change(rate1h_float)
            rate1h_msg = str(locale.format("%.2f", rate1h_float, True))

            btc_price_msg = "$" + str(locale.format("%.2f", float(btc_data_dict["price"]), True))

            msg_threshold = "\nBTC price rise alert: " + rate1h_msg + "%" + rate1h_emoji \
                            + "\nBTC price now at: " + btc_price_msg + "\n"

            send_message(msg=msg_threshold)

        # Fetch the price and rate of change for every time_interval
        time.sleep(config.TIME_INTERVAL)

# Function to send_message through Telegram
def send_message(msg):
    for id, bot in mybots.items():
        bot.send_message(id, text=msg)

# Function to fetch BTC data from CoinMarketCap
def fetch_data_from_coinmarketcap_api():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    query = "?symbol=" + config.MARKET_SYMBOL + "&convert=" + config.CURRENCY_ISO
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": config.CMC_API_KEY
    }
    
    # Make a request to the coinmarketcap api
    response = requests.get(url + query, headers=headers)
    response_json = response.json()
    
    # Extract the bitcoin price from the json data
    btc_data = response_json["data"][config.MARKET_SYMBOL]

    btc_data_dict = {}

    # Set most relevant information
    btc_data_dict["price"] = btc_data["quote"][config.CURRENCY_ISO]["price"]
    btc_data_dict["percent_change_1h"] = btc_data["quote"][config.CURRENCY_ISO]["percent_change_1h"]
    btc_data_dict["percent_change_24h"] = btc_data["quote"][config.CURRENCY_ISO]["percent_change_24h"]
    btc_data_dict["percent_change_7d"] = btc_data["quote"][config.CURRENCY_ISO]["percent_change_7d"]
    btc_data_dict["market_cap_dominance"] = btc_data["quote"][config.CURRENCY_ISO]["market_cap_dominance"]
    btc_data_dict["market_cap"] = btc_data["quote"][config.CURRENCY_ISO]["market_cap"]

    return btc_data_dict

# Compare percent and add an emoji
def parse_price_change(percent):
    emoji = ""

    if percent > 20:
        emoji = emojize(" :rocket:", use_aliases=True)
    elif percent <= -20:
        emoji = emojize(" :sos:", use_aliases=True)
    elif percent < 0:
        emoji = emojize(" :small_red_triangle_down:", use_aliases=True)
    elif percent > 0:
        emoji = emojize(" :white_check_mark:", use_aliases=True)

    return emoji

# Error handler function
def error(update, context):
    logging.error(f"Update {update} caused error {context.error}")