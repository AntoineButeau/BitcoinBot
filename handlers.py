import config
import requests
import time
import logging
import locale
from emoji import emojize

def start_command(update, context):
    update.message.reply_text("Hello there! This bot checks the BTC price every hour and sends alerts if it drops or rise by more than 5%")

def help_command(update, context):
    update.message.reply_text("This bot doesn't do much else yet. Try /price to get latest BTC market information or /satoshi to get a link to the Bitcoin whitepaper")

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

def price_command(update, context):
    update.message.reply_text(get_btc_market_information())

def satoshi_whitepaper_command(update, context):
    update.message.reply_text(text="<a href='https://bitcoin.org/bitcoin.pdf'>Satoshi Whitepaper</a>",parse_mode="HTML")

# Function to get BTC price
def fetch_data_from_coinmarketcap_api():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    query = '?symbol=' + config.MARKET_SYMBOL + '&convert=' + config.CURRENCY_ISO
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.CMC_API_KEY
    }
    
    # Make a request to the coinmarketcap api
    response = requests.get(url + query, headers=headers)
    response_json = response.json()
    
    # Extract the bitcoin price from the json data
    btc_data = response_json['data'][config.MARKET_SYMBOL]

    btc_data_dict = {}

    btc_data_dict["price"] = btc_data['quote'][config.CURRENCY_ISO]['price']
    btc_data_dict["percent_change_1h"] = btc_data['quote'][config.CURRENCY_ISO]['percent_change_1h']
    btc_data_dict["percent_change_24h"] = btc_data['quote'][config.CURRENCY_ISO]['percent_change_24h']
    btc_data_dict["percent_change_7d"] = btc_data['quote'][config.CURRENCY_ISO]['percent_change_7d']
    btc_data_dict["market_cap_dominance"] = btc_data['quote'][config.CURRENCY_ISO]['market_cap_dominance']
    btc_data_dict["market_cap"] = btc_data['quote'][config.CURRENCY_ISO]['market_cap']

    return btc_data_dict

def get_btc_market_information():

    btc_data_dict = fetch_data_from_coinmarketcap_api()
    
    # Get BTC price
    btc_price = '$' + str(locale.format("%.2f", float(btc_data_dict["price"]), True))

    #1 hour price change with emoji
    rate1h_float = btc_data_dict["percent_change_1h"]
    rate1h_emoji = parse_price_change(rate1h_float)
    rate1h = locale.format('%.2f', rate1h_float, True)

    #24 hour price change with emoji
    rate24h_float = btc_data_dict["percent_change_24h"]
    rate24h_emoji = parse_price_change(rate24h_float)
    rate24h = locale.format('%.2f', rate24h_float, True)

    #7 days price change with emoji
    rate7d_float = btc_data_dict["percent_change_7d"]
    rate7d_emoji = parse_price_change(rate7d_float)
    rate7d = locale.format('%.2f', rate7d_float, True)

    #Get marketcap dominance
    btc_dominance = str(btc_data_dict["market_cap_dominance"])

    #Get marketcap 
    btc_market_cap = '$' + str(locale.format("%.2f", float(btc_data_dict["market_cap"]), True))

    msg_market_information = '\nPrice: ' + btc_price \
                                 + '\nLast 1 hour change: ' + rate1h + '%' + rate1h_emoji \
                                 + '\nLast 24 hours change: ' + rate24h + '%' + rate24h_emoji \
                                 + '\nLast 7 days change: ' + rate7d + '%' + rate7d_emoji \
                                 + '\nBTC dominance: ' + btc_dominance \
                                 + '\nMarket Cap: ' + btc_market_cap + '\n'

    return msg_market_information

# Compare percent and add an emoji adequate
def parse_price_change(percent):
    emoji = ''

    if percent > 20:
        emoji = emojize(' :rocket:', use_aliases=True)
    elif percent <= -20:
        emoji = emojize(' :sos:', use_aliases=True)
    elif percent < 0:
        emoji = emojize(' :small_red_triangle_down:', use_aliases=True)
    elif percent > 0:
        emoji = emojize(' :white_check_mark:', use_aliases=True)

    return emoji

# Function to get the percentage of change vs. threshold TODO include % change
def determine_price_percentage_change_against_threshold():
    while True:

        # Get 1h percentage of change
        btc_data_dict = fetch_data_from_coinmarketcap_api()
        rate1h = btc_data_dict["percent_change_1h"]

        # If the percentage of change falls below threshold, send an immediate msg
        if rate1h <= config.LOWER_THRESHOLD:
            btc_price = '$' + str(locale.format("%.2f", float(btc_data_dict["price"]), True))
            send_message(chat_id=config.CHAT_ID, msg=f'BTC Price Drop Alert: {btc_price}')

        # If the percentage of change rises above threshold, send an immediate msg
        if rate1h >= config.UPPER_THRESHOLD:
            btc_price = '$' + str(locale.format("%.2f", float(btc_data_dict["price"]), True))
            send_message(chat_id=config.CHAT_ID, msg=f'BTC Price Rise Alert: {btc_price}')

        # Fetch the price and rate of change for every time_interval
        time.sleep(config.TIME_INTERVAL)

# Function to send_message through Telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"

    # Send the msg
    requests.get(url)

