#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
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
        user_data['body'] = None
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
        writer(bot, user.id, user_data, 'new')
    else:
        bot.send_message(chat_id=user.id, text="Bad restart")

def get(bot, update, user_data):
    user.id = update.message.from_user.id
    msg = update.message.text
    if user_data['caption'] is True:
        user_data['caption'] = msg
        answer = "عنوان متن تنظیم شد!"
    elif user_data['body'] is True:
        user_data['body'] = msg
        answer = "متن اصلی تنظیم شد!"
    elif user_data['author'] is True:
        user_data['author'] = msg
        answer = "نام صاحب سخن تنظیم شد!"
    else:
        answer = "برای ثبت پَند جدید از دستور زیر استفاده کنید:\n/new"
    bot.send_message(chat_id=user.id, text=answer)

def writer(bot, to, user_data, method):
    if user_data['caption'] is None:
	       user_data['caption'] = "هنوز چیزی ثبت نشده!"
    if user_data['body'] is None:
	       user_data['body'] = "هنوز متنی ثبت نشده!"
    if user_data['author'] is None:
	       user_data['author'] = "هنوز اسمی وارد نشده!"

    message = "عنوان:\n{0}\n\nمتن:\n{1}\n\nصاحب اثر:\n{2}\n\nبعد از پر کردن قسمت ها، دکمه *ثبت* را لمس نمیایید.".format(user_data['caption'], user_data['body'], user_data['author'])

    button_list = [[InlineKeyboardButton(text="عنوان", callback_data='caption')],
            [InlineKeyboardButton(text="صاحب سخن", callback_data='author'),
            InlineKeyboardButton(text="*متن", callback_data='body')],
            [InlineKeyboardButton(text="ثبت", callback_data='submit')]]

    reply_markup = InlineKeyboardMarkup(button_list)

    if method == 'new':
        bot.send_message(chat_id=to, text=message, reply_markup=reply_markup,
        disable_web_page_preview=True)
    elif method == 'edit':
        pass

def callback(bot, update, user_data):
    chat_id = update.callback_query.message.chat.id
    if update.callback_query.data == "caption":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="عنوان متن:")
        user_data['caption'] = True
        answer = "عنوان کوتاهی برای متن وارد کنید:"
    elif update.callback_query.data == "body":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="متن اصلی:")
        user_data['body'] = True
        answer = "متن اصلی را بنویسید:"
    elif update.callback_query.data == "author":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="صاحب سخن:")
        user_data['author'] = True
        answer = "نام صاحب سخن را وارد کنید:"
    elif update.callback_query.data == "submit":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="در حال ثبت ...")
        if user_data['body'] is not None:
            text = user_data['body']
            if user_data['caption'] is not None:
                text = user_data['caption'] + '\n' + text
            if user_data['author'] is not None:
                text = text + '\n' + user_data['author']
            answer = "ثبت شد!\nبعد از بازبینی، در کانال منتشر میشود.\n"+text
        else:
            answer = "برای ثبت، وارد کردن متن اصلی الزامی میباشد."
    else:
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Bad request")
        answer = "لطفا فقط از طریق دکمه های شیشه ای درخواست خود را ارسال کنید!"
    bot.send_message(chat_id=chat_id, text=answer)

if __name__ == "__main__":
    #start
    start_command = CommandHandler('start', start, pass_user_data=True)
    create_command = CommandHandler('new', create, pass_user_data=True)
    callback_handler = CallbackQueryHandler(callback, pass_user_data=True)
    user_message_handler = MessageHandler(Filters.text, get, pass_user_data=True)

    dispatcher.add_handler(start_command)
    dispatcher.add_handler(create_command)
    dispatcher.add_handler(callback_handler)
    dispatcher.add_handler(user_message_handler)

    print("READY TO USE!")

    updater.start_polling()
    updater.idle()
