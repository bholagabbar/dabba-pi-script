import requests
from pymongo import MongoClient

def getMongoClient():
    return MongoClient(host=os.environ['HOST'], port=int(os.environ['PORT']),
                       username=os.environ['USER'], password=os.environ['PASS']) #add params

def send_to_API(data):
    URL = "http://dabba.us-west-2.elasticbeanstalk.com/bins/"
    r = requests.post(URL, data)

def get_username(macID):
    client = getMongoClient()
    admin_db = client.admin
    posts = admin.posts
    username = posts.find_one({"U_ID": str(macID)})['USER_NAME']
    return username

def get_location(macID):
    client = getMongoClient()
    telegram_db = client.telegram_db
    posts = telegram_db.posts
    lat = posts.find_one({"U_ID": str(macID)})['LAT']
    lon = posts.find_one({"U_ID": str(macID)})['LON']
    return lat, lon

