import json
import os
from pickle import load

import telebot
from pymongo import MongoClient
from telebot import types

with open('config.json', 'r') as json_config_file:
    configFile = json.load(json_config_file)

for k, v in configFile.iteritems():
    os.environ[k] = v

client = MongoClient(host=os.environ['HOST'], port=int(os.environ['PORT']), username=os.environ['USER'], password=os.environ['PASS'])
# client = MongoClient()
db = client.telegram_db
text = load(open('text.txt', 'rb'))

markup = types.ReplyKeyboardMarkup()
start = types.KeyboardButton('/start')
location = types.KeyboardButton('/location')
reset = types.KeyboardButton('/reset')
status = types.KeyboardButton('/status')
markup.row(start, location)
markup.row(reset, status)

token = "506400947:AAFaKrX-EFVhM-O1e6rV5XyWMzVWtMB1Wdo"

bot = telebot.TeleBot(token)
async_bot = telebot.AsyncTeleBot(token)
config_dict = dict()

class telegram: #ADD PI-CLIENT VALIDATION TO EACH!

    def __init__(self):  # add Boolean variable, MAC ID of Pi, OR SERVER SIDE CODE???
        if os.path.isfile('config.p'):
            config_dict = load(open('config.p', 'rb'))

    @bot.message_handler(commands=['start'])
    def first_start(message):
        print message
        posts = db.posts
        if posts.find_one({"C_ID": str(message.from_user.id)}) is None:
            config_dict.update({"C_ID": message.from_user.id})
            post = {"C_ID": str(message.from_user.id),
                    "USER_NAME": str(message.from_user.username),
                    "U_ID": None,
                    "LAT": None,
                    "LONG": None,
                    "URL": None}
            posts.insert_one(post)
            bot.reply_to(message, text['start'], reply_markup=markup)
        else:
            bot.reply_to(message, "Hello", reply_markup=markup)
        # dump(message, open('message.p', 'wb'))

    def send_message(self, chat_id, message):
        async_bot.send_message(chat_id, message)

    @bot.message_handler(commands=['location'])
    def location_request(message):
        bot.reply_to(message, text['location_request'])

    @bot.message_handler(commands=['reset'])
    def reset(message):
        try:
            posts = db.posts
            posts.delete_one({"C_ID": str(message.from_user.id)})
            bot.reply_to(message, "Reset successfully")
        except:
            bot.reply_to(message, "Error")

    @bot.message_handler(commands=['status'])
    def status(message):
        try:
            posts = db.posts
            print posts.find_one({"C_ID": str(message.from_user.id)})
            url = posts.find_one({"C_ID": str(message.from_user.id)})['URL']
            bot.reply_to(message, str(url))
        except:
            bot.reply_to(message, "Error")

    @bot.message_handler(content_types=['text'])
    def mac_ID(message):
        try:
            if not db.posts.find_one({"C_ID": str(message.from_user.id)}) is None:
                posts = db.posts
                posts.update_one({'C_ID': str(message.from_user.id)}, {"$set": {'U_ID': str(message.text)}})
                bot.reply_to(message, "MAC ID successfully set!")
                print db.posts.find_one({"C_ID": str(message.from_user.id)})
            else:
                bot.reply_to(message, "Error")
                print db.posts.find_one({"C_ID": str(message.from_user.id)})
        except:
            bot.reply_to(message, "Error")

    @bot.message_handler(content_types=['location'])
    def get_location(message):
        try:
            if not db.posts.find_one({"C_ID": str(message.from_user.id)}) is None:
                posts = db.posts
                location_lat, location_long = message.location.latitude, message.location.longitude
                posts.update_one({'C_ID': str(message.from_user.id)}, {"$set": {"LAT": location_lat}})
                posts.update_one({'C_ID': str(message.from_user.id)}, {"$set": {"LONG": location_long}})
                # dump(config_dict, open('config.p', 'wb'))
                bot.reply_to(message, text['location_received'].format(location_lat, location_long))
            else:
                bot.reply_to(message, "Error")

        except:
            bot.reply_to(message, "Error")


    def poll(self):
        print "Telegram API Running"
        bot.polling(none_stop=True)
