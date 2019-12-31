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
from datetime import timedelta, datetime, date
from pytz import timezone

# Using US/Eastern time
est_timezone = timezone('US/Eastern')

# TinyDB 
from tinydb import TinyDB, Query
main_potd_db = TinyDB('main_potd_db.json')
old_potd_db = TinyDB('old_potd_db.json')

# Datetime Parser
from dateutil.parser import parse

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

# DateTime format to use everywhere
fmt = '%Y-%m-%d %H:%M:%S'
date_fmt = '%Y-%m-%d'

# Typing animation to show to user to imitate human interaction
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id = update.effective_message.chat_id, action = action)
            return func(bot, update, **kwargs)
        return command_func
    return decorator

send_typing_action = send_action(ChatAction.TYPING)

# '/start' command
@send_typing_action
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hello! Thank you for starting me! Use the /picture command to see today's NASA Image of the Day!")

    print(datetime.now(est_timezone).strftime(fmt))
    print("User {} and ID {} started the bot!".format(update.message.chat_id, str(update.message.from_user.username)))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# '/picture' command
@send_typing_action
def pictureoftheday_message(bot, update):

    # A new user has invoked the picture command since the chat_id cannot be found in database
    if main_potd_db.contains(Query()['chat_id'] == update.message.chat_id) == False:
        main_potd_db.insert({'chat_id': update.message.chat_id, 'time': str(datetime.now(est_timezone).strftime(fmt)), 'username': update.message.from_user.username})

        nasa_data = requests.get(nasa_url).json()
        title = nasa_data['title']
        explanation = nasa_data['explanation']
        if 'image' in nasa_data['media_type']:
            image = nasa_data['hdurl']
            bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(title), parse_mode = 'HTML')
            bot.send_photo(chat_id = update.message.chat_id, photo = image)
            bot.send_message(chat_id = update.message.chat_id, text = explanation)
            bot.send_message(chat_id = update.message.chat_id, text = '<b> NEW! </b> You can now access old pictures of the day! Type for example: <code> /old_picture 13 Jan 2005 </code>', parse_mode = 'HTML')
            print("A new user {} and ID {} called the /picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
        elif 'video' in nasa_data['media_type']:
            video = nasa_data['url']
            bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(title), parse_mode = 'HTML')
            bot.send_message(chat_id = update.message.chat_id, text = video)
            bot.send_message(chat_id = update.message.chat_id, text = explanation)
            bot.send_message(chat_id = update.message.chat_id, text = '<b> NEW! </b> You can now access old pictures of the day! Type for example: <code> /old_picture 13 Jan 2005 </code>', parse_mode = 'HTML')
            print("A new user {} and ID {} called the /picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
        else:
            bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")
            print("A new user {} and ID {} called the /picture command and an error occured!".format(update.message.chat_id, str(update.message.from_user.username)))
    # If user exists, search the last time they invoked the picture command
    elif main_potd_db.contains(Query()['chat_id'] == update.message.chat_id) == True:
        user = Query()
        result = main_potd_db.search((user.chat_id == update.message.chat_id) & (user.time != str(0)))
        time_getter = [sub['time'] for sub in result]
        print(time_getter[0])

        old_time = datetime.strptime(str(time_getter[0]), fmt)
        current_time = datetime.strptime(str(datetime.now(est_timezone).strftime(fmt)), fmt)

        # Calculate how much time has passed since we served the image
        minutes_diff = (current_time - old_time).total_seconds() / 60.0

        # If more than 10 minutes have passed, they can reuse the command
        if int(minutes_diff) >= 0:
            main_potd_db.upsert({'time': str(datetime.now(est_timezone).strftime(fmt)), 'username': str(update.message.from_user.username)}, Query()['chat_id'] == update.message.chat_id)

            nasa_data = requests.get(nasa_url).json()
            title = nasa_data['title']
            explanation = nasa_data['explanation']
            if 'image' in nasa_data['media_type']:
                image = nasa_data['hdurl']
                bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(title), parse_mode = 'HTML')
                bot.send_photo(chat_id = update.message.chat_id, photo = image)
                bot.send_message(chat_id = update.message.chat_id, text = explanation)
                bot.send_message(chat_id = update.message.chat_id, text = '<b> NEW! </b> You can now access old pictures of the day! Type for example: <code> /old_picture 13 Jan 2005 </code>', parse_mode = 'HTML')
                print("User {} and ID {} called the /picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
            elif 'video' in nasa_data['media_type']:
                video = nasa_data['url']
                bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(title), parse_mode = 'HTML')
                bot.send_message(chat_id = update.message.chat_id, text = video)
                bot.send_message(chat_id = update.message.chat_id, text = explanation)
                bot.send_message(chat_id = update.message.chat_id, text = '<b> NEW! </b> You can now access old pictures of the day! Type for example: <code> /old_picture 13 Jan 2005 </code>', parse_mode = 'HTML')
                print("User {} and ID {} called the /picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
            else:
                bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")
                print("User {} and ID {} called the /picture command and an error occured!".format(update.message.chat_id, str(update.message.from_user.username)))
        else:
            bot.send_message(chat_id = update.message.chat_id, text = "You're doing that too much. Please try again in {} minute(s)!".format(10 - int(minutes_diff)))
            print("User {} and ID {} spammed the /picture command and hit a cooldown!".format(update.message.chat_id, str(update.message.from_user.username)))
    else:
        pass

pictureoftheday_message_handler = CommandHandler('picture', pictureoftheday_message)
dispatcher.add_handler(pictureoftheday_message_handler)

@send_typing_action
def old_picture(bot, update, args):
    if args:
        user_input = "-".join(args)
        parsed_user_input = parse(user_input)
        user_input_string = str(parsed_user_input) 

        year = user_input_string[0:4]
        month = user_input_string[5:7]
        day = user_input_string[8:10]

        start_date = date(1995, 6, 16)

        entered_date = date(int(year), int(month), int(day))

        end = (datetime.now(est_timezone) - timedelta(1)).strftime(date_fmt)
        end_date = date(int(end[0:4]), int(end[5:7]), int(end[8:10]))

        if start_date <= entered_date <= end_date:
            if old_potd_db.contains(Query()['chat_id'] == update.message.chat_id) == False:
                old_potd_db.insert({'chat_id': update.message.chat_id, 'time': str(datetime.now(est_timezone).strftime(fmt)), 'username': update.message.from_user.username})

                old_pictures_url = 'https://api.nasa.gov/planetary/apod?api_key={}&date={}-{}-{}'.format(config.api_key, year, month, day)

                old_picture_data = requests.get(old_pictures_url).json()

                old_picture_title = old_picture_data['title']
                old_picture_explanation = old_picture_data['explanation']

                if 'image' in old_picture_data['media_type']:
                    old_image = old_picture_data['hdurl']
                    bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(old_picture_title), parse_mode = 'HTML')
                    bot.send_photo(chat_id = update.message.chat_id, photo = old_image)
                    bot.send_message(chat_id = update.message.chat_id, text = old_picture_explanation)
                    print("A user {} and ID {} called the /old_picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
                elif 'video' in old_picture_data['media_type']:
                    old_video = old_picture_data['url']
                    bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(old_picture_title), parse_mode = 'HTML')
                    bot.send_message(chat_id = update.message.chat_id, text = old_video)
                    bot.send_message(chat_id = update.message.chat_id, text = old_picture_explanation)
                    print("A user {} and ID {} called the /old_picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
                else:
                    bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")
                    print("A user {} and ID {} called the /old_picture command and an error occured!".format(update.message.chat_id, str(update.message.from_user.username)))
            
            elif old_potd_db.contains(Query()['chat_id'] == update.message.chat_id) == True:
                old_picture_user = Query()
                result = old_potd_db.search((old_picture_user.chat_id == update.message.chat_id) & (old_picture_user.time != str(0)))
                time_getter = [sub['time'] for sub in result]
                print(time_getter[0])

                old_time = datetime.strptime(str(time_getter[0]), fmt)
                current_time = datetime.strptime(str(datetime.now(est_timezone).strftime(fmt)), fmt)

                # Calculate how much time has passed since we served the image
                minutes_diff = (current_time - old_time).total_seconds() / 60.0

                if int(minutes_diff) >= 0:
                    old_potd_db.upsert({'time': str(datetime.now(est_timezone).strftime(fmt)), 'username': str(update.message.from_user.username)}, Query()['chat_id'] == update.message.chat_id)

                    old_pictures_url = 'https://api.nasa.gov/planetary/apod?api_key={}&date={}-{}-{}'.format(config.api_key, year, month, day)

                    old_picture_data = requests.get(old_pictures_url).json()

                    old_picture_title = old_picture_data['title']
                    old_picture_explanation = old_picture_data['explanation']

                    if 'image' in old_picture_data['media_type']:
                        old_image = old_picture_data['hdurl']
                        bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(old_picture_title), parse_mode = 'HTML')
                        bot.send_photo(chat_id = update.message.chat_id, photo = old_image)
                        bot.send_message(chat_id = update.message.chat_id, text = old_picture_explanation)
                        print("A user {} and ID {} called the /old_picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
                    elif 'video' in old_picture_data['media_type']:
                        old_video = old_picture_data['url']
                        bot.send_message(chat_id = update.message.chat_id, text = '<b>{}</b>'.format(old_picture_title), parse_mode = 'HTML')
                        bot.send_message(chat_id = update.message.chat_id, text = old_video)
                        bot.send_message(chat_id = update.message.chat_id, text = old_picture_explanation)
                        print("A user {} and ID {} called the /old_picture command!".format(update.message.chat_id, str(update.message.from_user.username)))
                    else:
                        bot.send_message(chat_id = update.message.chat_id, text = "Sorry, I couldn't deliver the image / video! An error occured!")
                        print("A user {} and ID {} called the /old_picture command and an error occured!".format(update.message.chat_id, str(update.message.from_user.username)))

                else:
                    bot.send_message(chat_id = update.message.chat_id, text = "You're doing that too much. Please try again in {} minute(s)!".format(2 - int(minutes_diff)))
                    print("User {} and ID {} spammed the /old_picture command and hit a cooldown!".format(update.message.chat_id, str(update.message.from_user.username)))
            else:
                pass
        else:
            bot.send_message(chat_id = update.message.chat_id, text = "Only dates between 16 June 1995 and {} are supported. Please try again!".format((datetime.now(est_timezone) - timedelta(1)).strftime('%d %B %Y')))
    else:
        bot.send_message(chat_id = update.message.chat_id, text = "Please enter a date after the command! For example: <code>/old_picture 20 Feb 2008 </code>", parse_mode = 'HTML')

old_picture_handler = CommandHandler('old_picture', old_picture, pass_args = True)
dispatcher.add_handler(old_picture_handler)

# Unknown command for error handling
@send_typing_action
def unknown(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="Sorry, I didn't understand that command! Please type /picture!")

    print(datetime.now(est_timezone))
    print("User {} and ID {} called an unknown command!".format(update.message.chat_id, str(update.message.from_user.username)))

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Module to start getting data
print("Bot started!")
updater.start_polling()
updater.idle()