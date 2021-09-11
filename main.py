import config
import handlers
import logging

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

def main():
    #Create a Bot object
    updater = Updater(config.BOT_TOKEN)

    #Hand
    handlers.btc_price_threshold()

    #Start the Bot start_polling() method
    #Keep the Bot listening using idle() method
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
