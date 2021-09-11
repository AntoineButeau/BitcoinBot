import os
import requests
import time

from telegram import Update #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

#global variables
cmc_api_key = os.getenv("CMC_TOKEN")
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv ("CHAT_TOKEN")
lower_threshold = 44500 #Bitcoin lower price threshold - TODO, need to take into account currency and latest price, probably also doesnt fit the use case I'm trying to achieve, so need to take into account historical price somewhat
upper_threshold = 46000 #Bitcoin upper threshold
time_interval = 10 * 60 # in seconds, 10 minutes time interval

#Function when user starts the bot
def start_command(update: Update, context: CallbackContext) -> None:
  pass

#Function to get BTC price
def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_api_key
    }
    
    #Make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    #Extract the bitcoin price from the json data - TODO consider user currency when starting
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']

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

    #Handle BTC pricing
    while True:
        price = get_btc_price()

        #If the price falls below threshold, send an immediate msg
        if price < lower_threshold:
             send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: {price}')

        if price > upper_threshold:
             send_message(chat_id=chat_id, msg=f'BTC Price Rise Alert: {price}')

        #Fetch the price for every time_interval
        time.sleep(time_interval)

    #Start the Bot start_polling() method
    #Keep the Bot listening using idle() method
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()