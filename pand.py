#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging

def start(bot, update):
    user.id = update.message.from_user.id
    hello = "به پَند بات خوش آمدید!\nبا این ربات میتوانید پَند های آموزنده ای که میشنوید را در کانال ما به اشتراک بگذارید."
    bot.send_message(chat_id=user.id, text=hello)

if __name__ == "__main__":
    class User:
        def __init__(self):
            self.id = None
            self.fname = None
            self.lname = None
            self.uname = None

    user = User()

    home_dir = '/home/pat/Desktop/projects/python/bots/pand/'
    log_location =  home_dir+'logs/bot.log'
    logging.basicConfig(filename=log_location ,format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)

    updater = Updater(token="628324666:AAHBU94JUKqBA-EsKxAyjaOmIkVq7DDZwQU")
    dispatcher = updater.dispatcher

    #start
    start_command = CommandHandler('start', start)
    dispatcher.add_handler(start_command)

    print("READY TO USE!")

    updater.start_polling()
    updater.idle()
