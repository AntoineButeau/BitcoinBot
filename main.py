import requests
import time
import bitcoinbot.config as config

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

#Function when user starts the bot
def start_command(update: Update, context: CallbackContext) -> None:
    pass

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

def main():
    #Create a Bot object
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    #Bot start handler
    dispatcher.add_handler(CommandHandler("start", start_command))

    #Handle BTC price
    btc_price_threshold()

    #Start the Bot start_polling() method
    #Keep the Bot listening using idle() method
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
