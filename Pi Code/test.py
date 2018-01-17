import telebot
from telebot import types
import json
import pickle
bot = telebot.TeleBot("251903620:AAGQSJErICuLtrEEx_Enm90pyv-KpCNCbP0")

@bot.message_handler(content_types=['location'])
def send_welcome(message):
    lat, lon = message.location.latitude, message.location.longitude
    print lat, lon
    return lat, lon
bot.polling()