#!/usr/bin/env python

import re
import telebot, sys
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#import logging

SHOW_BTN = False
PROXY = False

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

if PROXY:
	from telebot import apihelper
	apihelper.proxy = {'https': 'socks5h://user:pass@ip'}

BOT_TOKEN=''
DESTINATION=sys.argv[1]
SUBJECT=sys.argv[2]
MESSAGE=sys.argv[3]

def extractIPs(fileContent):
    pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([ (\[]?(\.|dot)[ )\]]?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
    ips = [each[0] for each in re.findall(pattern, fileContent)]   
    for item in ips:
        location = ips.index(item)
        ip = re.sub("[ ()\[\]]", "", item)
        ip = re.sub("dot", ".", ip)
        ips.remove(item)
        ips.insert(location, ip) 
    return ips[0]

#chat -1001397537526
#MESSAGE = MESSAGE.replace('/n','\n')
tb = telebot.TeleBot(BOT_TOKEN)
if SHOW_BTN:
	IP = extractIPs(MESSAGE)
	keyboard = InlineKeyboardMarkup()
	url_btn = InlineKeyboardButton(text="Open", url=str(IP))
	keyboard.add(url_btn)
	
	tb.send_message(DESTINATION ,SUBJECT + '\n' + MESSAGE, reply_markup = keyboard)
else:
	tb.send_message(DESTINATION ,SUBJECT + '\n' + MESSAGE)