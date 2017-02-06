#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk
import datetime
import telegram
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError)

def get_lunch_text():
	session = vk.Session()
	api = vk.API(session)
	posts = api.wall.get(domain='reddoorpub', count=10)

	now_date = datetime.datetime.now().date()

	res = 'Пока не вывесили меню на сегодня :('

	for post in posts:
		if isinstance(post, dict):
			post_text = post['text']
			post_date = datetime.date.fromtimestamp(post['date'])
			lunch_template = u"Друзья! Сегодня на ланч у нас"

			if post_date >= now_date and lunch_template in post_text:
				res = post_text
				break
	return res

def start(bot, update):
	msg_text = get_lunch_text()
	bot.sendMessage(chat_id=update.message.chat_id, text=msg_text)

def setup_logging():
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print "Unauthorized"
    except BadRequest:
        print "BadRequest"
        print error
    except TimedOut:
        print "TimedOut"
    except NetworkError:
        print "NetworkError"
    except ChatMigrated as e:
        print "ChatMigrated"
    except TelegramError:
        print error


setup_logging()

token = '236125004:AAFohdVnfvwwhpj2G8_SMJecYp9Uudlhw1w'
bot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

dispatcher.add_error_handler(error_callback)

updater.start_polling()