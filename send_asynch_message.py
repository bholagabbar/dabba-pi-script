from pymongo import MongoClient



def getMongoClient():
    return MongoClient(host=os.environ['HOST'], port=int(os.environ['PORT']),
                       username=os.environ['USER'], password=os.environ['PASS']) #add params


def send_message(user_name, message):
    client = getMongoClient()
    telegram = client.telegram_db.posts
    chat_id = telegram.find_one({"USER_NAME": str(user_name)})['C_ID']
    token = os.environ['KEY']
    async_bot = telebot.AsyncTeleBot(token)
    async_bot.send_message(chat_id, str(message))