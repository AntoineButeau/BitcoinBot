import os
import requests
import time

from telegram import Update #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

#global variables
cmc_api_key = os.getenv("CMC_TOKEN")
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv ("CHAT_TOKEN")
threshold = 30000 #Bitcoin price threshold - TODO, need to take into account currency and latest price
time_interval = 5 * 60 # in seconds, 5 minutes time interval

def start_command(update: Update, context: CallbackContext) -> None:
  pass

def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_api_key
    }
    
    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']

def main():
    # Create a Bot object
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # Bot start handler
    dispatcher.add_handler(CommandHandler("start", start_command))

    # Start the Bot start_polling() method
    # Keep the Bot listening using idle() method
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()