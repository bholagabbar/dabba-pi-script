import requests

def send_to_API(data):
    URL = "http://dabba.us-west-2.elasticbeanstalk.com/bins/"
    r = requests.post(URL, data)
