from pymongo import MongoClient



def getMongoClient():
    return MongoClient(os.environ['CHARTS_DB_HOST'], 27017) #add params


def send_message(user_name, message):
    client = getMongoClient()
    telegram = client.telegram_db.posts
    chat_id = telegram.find_one({"USER_NAME": str(user_name)})['C_ID']
    token = os.environ['TELEGRAM_KEY']
    async_bot = telebot.AsyncTeleBot(token)
    async_bot.send_message(chat_id, str(message))