import config
import handlers
import logging

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Function when user starts the bot
def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')

#Function when user types help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

#Echo the user message on noncommand command
def echo(update: Update, context: CallbackContext)  -> None:
    update.message.reply_text(update.message.text)

#Log errors caused by updates
def error(update: Update, context: CallbackContext)  -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    #Create a Bot object
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    #On different commands - Answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    #On noncommand - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    #log all errors
    dispatcher.add_error_handler(error)

    #Hand
    handlers.btc_price_threshold()

    #Start the Bot start_polling() method
    #Keep the Bot listening using idle() method
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
