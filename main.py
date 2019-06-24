#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

#import logging
import config
import telebot
from telebot import apihelper, types
from importer import Importer
import os

if config.proxy:
	apihelper.proxy = {'https': config.proxy_addr}

bot = telebot.TeleBot(config.bot_token)

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

def check_permission(uid):
	if uid not in config.users:
		return False
	return True

def file_ext(filename):
    return filename.split(".")[-1]

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Я тупая машина, и я ничего не умею")

@bot.message_handler(commands=['id', 'myid'])
def my_id(message):
	bot.send_message(message.chat.id, 'Твой ID: ' + str(message.chat.id))

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        if check_permission(message.from_user.id):
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            if file_ext(message.document.file_name) == 'csv':
                src='/tmp/'+message.document.file_name;
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message,"Added\n"+src)
                imp = Importer(src, config.zabbix_user, config.zabbix_pass, config.zabbix_api)
                imp.create_host()
                os.remove(src)
                bot.reply_to(message, imp.debug)
            else:
                bot.reply_to(message, "What is it?")
        else:
            pass
    except Exception as e:
        bot.reply_to(message,e )

if __name__ == '__main__':
	pid = str(os.getpid())
	pidf = config.pid
	try:		
		pidfile = open(pidf, 'w')
		pidfile.write(pid)
		pidfile.close()
		bot.polling(none_stop=True, interval=0, timeout=10)
	except Exception as e:
		print(e)
	finally:
		os.remove(pidf)