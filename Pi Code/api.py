import requests
import json
import os
from pymongo import MongoClient
from lights import strobe

def getMongoClient():
    host = os.environ.get('CHARTS_DB_HOST')
    port = 27017
    return MongoClient(host, port)  # add params


def send_data(data):
    URL = "http://dabba.us-west-2.elasticbeanstalk.com/bins/"
    r = requests.post(URL, data)
    try:
        response = json.loads(r.content, encoding='utf-8')
        print response
        if response['segregation'] == 'wrong':
            strobe()
    except Exception as e:
        print e
    print r

    URL = os.environ['WEB_ENDPOINT']
    message = dict()
    message['USER'] = 'piyush9620'
    message['MSG'] = data
    r = requests.post(URL, json.dumps(message))
    print r


def get_username(macID):
    client = getMongoClient()
    telegram_db = client.telegram_db
    posts = telegram_db.posts
    print posts
    username = posts.find_one({"U_ID": macID})['USER_NAME']
    client.close()
    return username


def get_location(macID):
    client = getMongoClient()
    telegram_db = client.telegram_db
    posts = telegram_db.posts
    print posts.find({})[0]
    print macID
    lat = posts.find_one({"U_ID": macID})['LAT']
    lon = posts.find_one({"U_ID": macID})['LONG']
    client.close()
    return str(lat), str(lon)


def get_type(macID):
    client = getMongoClient()
    telegram_db = client.telegram_db
    posts = telegram_db.posts
    bin_type = posts.find_one({"U_ID": macID})['TYPE']
    client.close()
    return str(bin_type)


def confirm_authentication(macID):
    print macID
    client = getMongoClient()
    telegram_db = client.telegram_db
    posts = telegram_db.posts
    result = posts.find_one({"U_ID": macID})
    print result
    print result['LAT']
    print result['LONG']
    print result['TYPE']
    client.close()
    try:
        if (result['LAT'] != None) and (result['LONG'] != None) and (result['TYPE'] != None):
            print "1"
            return False
        else:
            print "2"
            return True
    except:
        print "3"
        return True
