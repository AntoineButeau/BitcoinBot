import config
import handlers
import logging

from telegram.ext import Updater, CommandHandler  #upm package(python-telegram-bot)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logging.info('Starting Bot...')

def main():
    # Create a Bot object
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Bot commands
    dp.add_handler(CommandHandler('start', handlers.start_command))
    dp.add_handler(CommandHandler('help', handlers.help_command))
    dp.add_handler(
        CommandHandler('satoshi', handlers.satoshi_whitepaper_command))
    dp.add_handler(CommandHandler('price', handlers.price_command))

    # Log all errors
    dp.add_error_handler(handlers.error)

    # Start the Bot start_polling() method
    updater.start_polling()

    # Function to check if BTC price is above or below threshold and send message
    #dp.bot.sendMessage(text="test")
    handlers.get_price_percentage_change_against_threshold()
    

    # Keep the Bot listening using idle() method
    updater.idle()


if __name__ == '__main__':
    main()
