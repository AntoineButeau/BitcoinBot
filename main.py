import config
import handlers
import logging

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

def main():
    #Create a Bot object
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', handlers.start_command))
    dp.add_handler(CommandHandler('help', handlers.help_command))

    # Log all errors
    dp.add_error_handler(handlers.error)    

    #Start the Bot start_polling() method
    #Keep the Bot listening using idle() method
    updater.start_polling()
    handlers.btc_price_threshold()
    updater.idle()

if __name__ == '__main__':
    main()
