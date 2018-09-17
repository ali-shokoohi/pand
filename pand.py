#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import logging

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

def restart(user_data):
    try:
        user_data['caption'] = None
        user_data['text'] = None
        user_data['author'] = None
        return(True)
    except:
        return(False)

def start(bot, update, user_data):
    user.id = update.message.from_user.id
    user.fname = str(update.message.from_user.first_name).encode('utf-8').decode('utf-8')
    user.lname = str(update.message.from_user.last_name).encode('utf-8').decode('utf-8')
    user.uname = update.message.from_user.username
    hello = "به پَند بات خوش آمدید!\nبا این ربات میتوانید پَند های آموزنده ای که میشنوید را در کانال ما به اشتراک بگذارید."
    bot.send_message(chat_id=user.id, text=hello)
    restart(user_data)

def create(bot, update, user_data):
    erase = restart(user_data)
    user.id = update.message.from_user.id
    if (erase is True):
        message = """عنوان:\n*هنوز چیزی ثبت نشده!*\nمتن:\n*هنوز متنی ثبت نشده!*\nصاحب سخن:\n*هنوز اسمی وارد نشده!*
        \n\nبعد از پر کردن قسمت ها، دکمه *ثبت* را لمس نمیایید."""

        button_list = [[InlineKeyboardButton(text="عنوان", callback_data='caption')],
        [InlineKeyboardButton(text="صاحب سخن", callback_data='author'),
        InlineKeyboardButton(text="*متن", callback_data='text')],
        [InlineKeyboardButton(text="ثبت", callback_data='submit')]]

        reply_markup = InlineKeyboardMarkup(button_list)

        bot.send_message(chat_id=user.id, text=message, reply_markup=reply_markup ,
        disable_web_page_preview=True, parse_mode='MARKDOWN')
    else:
        bot.send_message(chat_id=user.id, text="Bad restart")

def get(bot, update, user_data):
    user.id = update.message.from_user.id
    if user_data['text'] is not None:
        pass
    else:
        pass

if __name__ == "__main__":
    #start
    start_command = CommandHandler('start', start, pass_user_data=True)
    create_command = CommandHandler('new', create, pass_user_data=True)

    dispatcher.add_handler(start_command)
    dispatcher.add_handler(create_command)

    print("READY TO USE!")

    updater.start_polling()
    updater.idle()
