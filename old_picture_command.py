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

from main_bot import updater, dispatcher, bot, send_typing_action

# Import time library
import time
from datetime import timedelta, datetime
from pytz import timezone
from dateutil.parser import parse

# Using US/Eastern time
est_timezone = timezone('US/Eastern')

# TinyDB 
from tinydb import TinyDB, Query
db = TinyDB('db.json')

# @send_typing_action
# def old_picture(update, context, bot):
#     user_input = "-".join(context.args)
#     parsed_user_input = parse(user_input)
#     user_input_string = str(parsed_user_input)

#     year = user_input_string[0:4]
#     month = user_input_string[5:7]
#     day = user_input_string[8:10]

#     old_pictures_url = 'https://api.nasa.gov/planetary/apod?api_key={}&date={}-{}-{}'.format(config.api_key, year, month, day)

#     old_picture_data = requests.get(old_pictures_url).json()

#     old_picture_title = old_picture_data['title']
#     old_picture_explanation = old_picture_data['explanation']

#     if 'image' in old_picture_data['media_type']:
#         old_image = old_picture_data['hdurl']
#         bot.send_message(chat_id = update.message.chat_id, text = old_picture_title)
#         bot.send_photo(chat_id = update.message.chat_id, photo = old_image)
#         bot.send_message(chat_id = update.message.chat_id, text = old_picture_explanation)
#         print("A new user {} and ID {} called the /old_picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
#     elif 'video' in old_picture_data['media_type']:
#         old_video = old_picture_data['url']
#         bot.send_message(chat_id = update.message.chat_id, text = old_picture_title)
#         bot.send_message(chat_id = update.message.chat_id, text = old_video)
#         bot.send_message(chat_id = update.message.chat_id, text = old_picture_explanation)
#         print("A new user {} and ID {} called the /old_picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
#     else:
#         bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")