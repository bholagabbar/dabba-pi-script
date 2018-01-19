import telebot
from telebot import types
import json
from pickle import load, dump
import os

text = load(open('text.txt', 'rb'))

markup = types.ReplyKeyboardMarkup()
start = types.KeyboardButton('/start')
location = types.KeyboardButton('/location')
reset = types.KeyboardButton('/reset')
status = types.KeyboardButton('/status')
markup.row(start, location)
markup.row(reset, status)

token = "251903620:AAGQSJErICuLtrEEx_Enm90pyv-KpCNCbP0"

bot = telebot.TeleBot(token)
async_bot = telebot.AsyncTeleBot(token)
config_dict = dict()

class telegram:
	
	def __init__(self): #add Boolean variable, MAC ID of Pi, OR SERVER SIDE CODE???
		if os.path.isfile('config.p'):
			config_dict = load(open('config.p', 'rb'))

	@bot.message_handler(commands=['start'])
	def first_start(message):
		config_dict.update({"C_ID":message.from_user.id})
		bot.reply_to(message, text['start'], reply_markup=markup)
		# dump(message, open('message.p', 'wb'))

	def send_message(self, chat_id, message):
		async_bot.send_message(chat_id, message)

	@bot.message_handler(commands=['location'])
	def location_request(message):
		bot.reply_to(message, text['location_request'])

	@bot.message_handler(commands=['reset'])
	def reset(message):
		bot.reply_to(message, text['reset'])

	@bot.message_handler(commands=['status'])
	def status(message):
		bot.reply_to(message, text['status'])

	@bot.message_handler(content_types=['location'])
	def get_location(message):
		location_lat, location_long = message.location.latitude, message.location.longitude
		config_dict.update({"LAT":location_lat})
		config_dict.update({"LONG":location_long})
		dump(config_dict, open('config.p', 'wb'))
		bot.reply_to(message, text['location_received'].format(location_lat, location_long))

	def poll(self):
		bot.polling()