import config
import requests
import time
import logging

def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')

def help_command(update, context):
    update.message.reply_text('Try typing anything and I will do my best to respond!')

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

#Function to get BTC price
def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    query = '?symbol=' + config.MARKET_SYMBOL + '&convert=' + config.CURRENCY_ISO
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.CMC_API_KEY
    }
    
    # make a request to the coinmarketcap api
    response = requests.get(url + query, headers=headers)
    response_json = response.json()
    # extract the bitcoin price from the json data
    btc_price = response_json['data'][config.MARKET_SYMBOL]

    return btc_price['quote'][config.CURRENCY_ISO]['price']

#Function to handle the price threshold
def btc_price_threshold():
    while True:
        price = get_btc_price()

        #If the price falls below threshold, send an immediate msg
        if price < config.LOWER_THRESHOLD:
            send_message(chat_id=config.CHAT_ID, msg=f'BTC Price Drop Alert: {price}')

        if price > config.UPPER_THRESHOLD:
            send_message(chat_id=config.CHAT_ID, msg=f'BTC Price Rise Alert: {price}')

        #Fetch the price for every time_interval
        time.sleep(config.TIME_INTERVAL)

#Function to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"

    #Send the msg
    requests.get(url)