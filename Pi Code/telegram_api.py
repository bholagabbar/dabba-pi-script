import telebot
from telebot import types
import json
import pickle
bot = telebot.TeleBot("251903620:AAGQSJErICuLtrEEx_Enm90pyv-KpCNCbP0")

text = pickle.load(open('text.txt', 'rb'))

markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('/start')
itembtnv = types.KeyboardButton('/location')
itembtnc = types.KeyboardButton('/reset')
itembtnd = types.KeyboardButton('/status')
markup.row(itembtna, itembtnv)
markup.row(itembtnc, itembtnd)

@bot.message_handler(commands=['start'])
def first_start(message):
	bot.reply_to(message, text['start'], reply_markup=markup)

@bot.message_handler(commands=['location'])
def first_start(message):
	bot.reply_to(message, text['location_request'])

@bot.message_handler(commands=['reset'])
def first_start(message):
	bot.reply_to(message, text['reset'], reply_markup=markup)

@bot.message_handler(commands=['status'])
def first_start(message):
	bot.reply_to(message, text['status'], reply_markup=markup)

@bot.message_handler(content_types=['location'])
def get_location(message):
	lat, lon = message.location.latitude, message.location.longitude
	bot.reply_to(message, text['location_received'].format(lat, lon))

bot.polling()