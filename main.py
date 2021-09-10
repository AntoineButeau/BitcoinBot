import os

from telegram import Update #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)


def start_command(update: Update, context: CallbackContext) -> None:
  pass

def main():
    updater = Updater(os.getenv("TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()