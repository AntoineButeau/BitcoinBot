## Bitcoin Price Notification in Telegram
A Telegram Bot to get notified when the BTC price changes drastically, so you can adjust your stacking sats strategy.

## What It Can Do?
- If the BTC price falls below or rises above a certain 1h percentage  `threshold`, it will send an immediate Telegram message.
- `/price` gets the latest  information from CoinMarketCap.
- `/satoshi` gets the link to the Bitcoin Whitepaper.
- `/start` and `/help` instruct the user on what the Bot can do.

## Inspiration
* [Quick-start Telegram Bot - Replit Docs](https://docs.replit.com/tutorials/18-telegram-bot#:~:text=To%20do%20this%2C%20start%20by,%2C%20click%20on%20%22start%22.)
* [How To Create A Telegram Bot With Python - CS Dojo](https://www.youtube.com/watch?v=NwBWW8cNCP4)
* [CryptoCoinsInfoBot v2](https://github.com/lytves/crypto-coins-info-bot-v2)
* [Bitcoin Price Tracker](https://github.com/leogaggl/bitcoin_price_tracker)
* [Premium Telegram Bot 2021](https://github.com/federicocotogno/premium_telegram_bot_2021)

## Prerequisites
To make this work, you will need the following:

* A [coinmarketcap.com](https://pro.coinmarketcap.com/) `api_key`.
* The [Telegram application](https://telegram.org/) and your account `chat_id`.
* A [Telegram Bot](https://core.telegram.org/bots) and its `token`.
* A Replit account. [Create one](https://replit.com/signup) if you haven't already.

## Limitations
* Need an "Always On" Repl to make sure the bot never falls asleep.

## 1) Getting CoinMarketCap API Key
Sign up or login on [pro.coinmarketcap.com](https://pro.coinmarketcap.com/).

You will then be taken to your account dashboard. There is a limit in using their API with their Basic Plan at **333 requests a day**. Good enough for us, but you might want to use their paid plan or look at other APIs products like Coindesk.

Click on `COPY KEY` button which will pop up when you over the `API Key` box. You can add this key in your **Replit Secrets (System environment variables)** with the key being `CMC_TOKEN` and the value being the `api_key` you just copied.

## 2) Telegram Bot and your Chat ID
Make sure you have the Telegram app installed on your phone/computer and you have an account created.

### Creating a Bot
You can use [BotFather](https://core.telegram.org/bots#6-botfather) to create new bot accounts and manage your existing bots:

* Search for BotFather in the Telegram app. You will see the BotFather with a blue verified tick next to it.
* Click on that bot and send the command `/newbot`. BotFather will ask for a `name` and `username`. 
* Then it will send you a congrats message which contains the `link to your bot` and the `authorization token` for your bot.

Copy that `authorization token` and add this in your **Replit Secrets** with the key being `BOT_TOKEN` and the value being the `authorization token` you just copied.

### Getting your chat_id
There is a limitation in the **python-telegram-bot** library we are going to use. You can only send a message in response to a user input or schedule a message for a specific time. 

In our case, we want to send a message when the percentage of change is above or below a certain `threshold` so we need the `chat_id` in order to bypass that limitation and send a message directly via the telegram API.

To get your `chat_id`, search in the Telegram App for `IDBot`. Click on that bot and type `/getid` which will get your `chat_id`.

Copy that `chat_id` and add this in your **Replit Secrets** with the key being `CHAT_TOKEN` and the value being the `chat_id` you just copied.

## 3) Files Description
### config.py
**Description:** Contains all the variables needed to interact with the APIs and run the bot.

* `CMC_API_KEY`: CoinMarketCap Pro API Key.
* `BOT_TOKEN`: Token of the Telegram bot.
* `CHAT_ID`: Token to send message and bypass **python-telegram-bot** limitations.
* `TIME_INTERVAL`: Do API requests to CoinMarketCap at a set time interval (in seconds). Currently set to 60 minutes, but you could lower it if you want to make sure to not miss a drop or a rise in value.
* `MARKET_SYMBOL`: Market symbol to pull from CoinMarketCap, currently set at `BTC` but you could change it to any coin you want to follow like `ETH`.
* `CURRENCY_ISO`: Currency to pull from CoinMarketCap. Currently set at `USD`, but you could change it to any currency  like `CAD`.
* `LOCALE`: Set locale for formatting numbers and text. Currently set at `en_US.UTF-8`, but you could change it to any country.
* `LOWER_THRESHOLD` and `UPPER_TRESHOLD`: Percentage thresholds to notify users. Currently set at +/- 5% but you could make it lower or higher depending on your needs. Note that CoinMarketCap returns the percentage change in this format -0.2509 for -0.25%.

### handlers.py
**Description:** Contains all the functions needed for the bot to handle user commands and send messages.
* `start_command(update, context)`: Function to handle user sending `/start` command to the bot.
* `help_command(update, context)`: Function to handle user sending `/help` command to the bot.
* `satoshi_whitepaper_command(update, context)`: Function to handle user sending `/satoshi` command to the bot. It will send the Bitcoin Whitepaper via a HTML link.
* `price_command(update, context)`: Function to handler user sending `/price` command to the bot. Function will call `get_btc_market_information()` which returns formatted text of latest CoinMarketCap information on Bitcoin.
* `get_btc_market_information()`: Function to set and format BTC market information to users. Function will call `fetch_data_from_coinmarketcap_api()` to get the data from CoinMarketCap API and `parse_price_change(percent)` to format some of the text with emojis. 
* `get_price_percentage_change_against_threshold()`: Function to get the percentage of change vs. threshold at a set time interval and send message if needed. Function will call `fetch_data_from_coinmarketcap_api()` to get the data from CoinMarketCap API and `parse_price_change(percent)` to format some of the text with emojis. 
* `send_message(chat_id, msg)`: Function to send_message through Telegram bypassing **python-telegram-bot** limitations.
* `fetch_data_from_coinmarketcap_api()`: Function to fetch BTC data from CoinMarketCap.
* `parse_price_change(percent)`:Function to parse price change and add emojis.
* `error(update, context)`: Error handler to log errors in console.

### main.py
**Description:** Create the bot, add handlers and run the bot.
* The updater is a class that will continuously check Telegram for new messages for our bot.
* When the updater gets a new message, it hands it over to the dispatcher. The dispatcher checks if we have an appropriate handler for the message. 
* Handler for `start`, `help`, `price`, `satoshi` are added
* We log all errors in console
* `updater.start_polling()` is used to tell the updater to start checking for new messages. start_polling is a non-blocking function. That means that the code won't halt execution here. It will just carry on until the program terminates.
* `updater.idle()` is used to keep the bot listening, since `updater.start_polling()` would execute and then immediately exit because there's nothing blocking it. `updater.idle()` block the script while the bot is listening.
* Note: `get_price_percentage_change_against_threshold()` is between `updater.start_polling()` and `updater.idle()` since we want to have the bot started before fetching data from CoinMarketCap to determine the price change against threshold. If you put the function before, the bot will not start properly.

## What's Next
* Have users set currency and locale based on their preference.
* Have users set the percentage threshold based on their own stacking sats strategy.
* Provide more analytics on market information so that users can make more informed decision on changing their stacking sats strategy.
* Provide a way for users to buy Bitcoin by referring to P2P exchange.
* Provide a weekly roundup for users to get market information via Telegram.
* Add Bitcoin Quiz where users can test their knowledge of Bitcoin and learn.
* Improve `satoshi` command where it would send quotes from the Bitcoin Whitepaper.
* Have users set the market symbol they want to pull from CoinMarketCap.
* Have users pull information on multiple market symbols and set thresholds depending on their preferred market symbols.