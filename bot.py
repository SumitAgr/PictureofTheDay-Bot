# -*- coding: utf-8 -*-
# Python-telegram-bot libraries
import telegram
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functools import wraps

# Logging and requests libraries
import logging
import requests

# Import token from config file
import config

# Import time library
import time
import datetime

# Importing the Updater object with token for updates from Telegram API
# Declaring the Dispatcher object to send information to user
# Creating the bot variable and adding our token
updater = Updater(token = config.token)
dispatcher = updater.dispatcher
bot = telegram.Bot(token = config.token)

# Logging module for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# NASA API
nasa_api_key = config.api_key
nasa_url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(nasa_api_key)

# Reply Keyboard
reply_keyboard = [['/picture 🖼']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard = True)

# Typing animation to show to user to imitate human interaction
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    return decorator

send_typing_action = send_action(ChatAction.TYPING)

# '/start' command
@send_typing_action
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hello there! Thank you for starting me! Use the /picture command to see today's NASA image of the day!", reply_markup = markup)

    print(datetime.datetime.now())
    print("User {} started the bot!".format(update.message.chat_id))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# '/picture' command
@send_typing_action
def pictureoftheday_message(bot, update):
    nasa_data = requests.get(nasa_url).json()
    title = nasa_data['title']
    explanation = nasa_data['explanation']
    if 'image' in nasa_data['media_type']:
        image = nasa_data['hdurl']
        bot.send_message(chat_id = update.message.chat_id, text = title)
        bot.send_photo(chat_id = update.message.chat_id, photo = image)
        bot.send_message(chat_id = update.message.chat_id, text = explanation)
    elif 'video' in nasa_data['media_type']:
        video = nasa_data['url']
        bot.send_message(chat_id = update.message.chat_id, text = title)
        bot.send_message(chat_id = update.message.chat_id, text = video)
        bot.send_message(chat_id = update.message.chat_id, text = explanation)
    else:
        bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")

    print(datetime.datetime.now())
    print("User {} called the /picture command!".format(update.message.chat_id))

pictureoftheday_message_handler = CommandHandler('picture', pictureoftheday_message)
dispatcher.add_handler(pictureoftheday_message_handler)

# Unknown command for error handling
@send_typing_action
def unknown(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="Sorry, I didn't understand that command! Please try again!")

    print(datetime.datetime.now())
    print("User {} called an unknown command!".format(update.message.chat_id))

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Module to start getting data
updater.start_polling()
updater.idle()