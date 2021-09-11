import os
import requests
import time

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

#global variables
cmc_api_key = os.getenv("CMC_TOKEN")
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_TOKEN")
market_symbol = 'BTC'
currency_iso = 'USD'
lower_threshold = 45500  #Bitcoin lower price threshold - TODO, need to take into account currency and latest price, probably also doesnt fit the use case I'm trying to achieve, so need to take into account historical price somewhat
upper_threshold = 46000  #Bitcoin upper threshold
time_interval = 30 * 60  # in seconds, 30 minutes time interval


#Function when user starts the bot
def start_command(update: Update, context: CallbackContext) -> None:
    pass

#Function to get BTC price
def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    query = '?symbol=' + market_symbol + '&convert=' + currency_iso
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_api_key
    }
    
    # make a request to the coinmarketcap api
    response = requests.get(url + query, headers=headers)
    response_json = response.json()
    # extract the bitcoin price from the json data
    btc_price = response_json['data'][market_symbol]

    return btc_price['quote'][currency_iso]['price']

#Function to handle the price threshold
def btc_price_threshold():
    while True:
        price = get_btc_price()

        #If the price falls below threshold, send an immediate msg
        if price < lower_threshold:
            send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: {price}')

        if price > upper_threshold:
            send_message(chat_id=chat_id, msg=f'BTC Price Rise Alert: {price}')

        #Fetch the price for every time_interval
        time.sleep(time_interval)

#Function to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    #Send the msg
    requests.get(url)

def main():
    #Create a Bot object
    updater = Updater(bot_token)
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
