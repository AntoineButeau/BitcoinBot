import config
import handlers

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

#Function when user starts the bot
def start_command(update: Update, context: CallbackContext) -> None:
    pass

def main():
    #Create a Bot object
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    #Bot start handler
    dispatcher.add_handler(CommandHandler("start", start_command))

    #Handle BTC price
    handlers.btc_price_threshold()

    #Start the Bot start_polling() method
    #Keep the Bot listening using idle() method
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
