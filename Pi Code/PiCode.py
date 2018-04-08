import logging
import datetime
import os
from pickle import dump
from time import sleep
from uuid import getnode as get_mac
import json

import RPi.GPIO as gp
from dropbox import Dropbox
from google.cloud import vision
from google.cloud.vision import types

from dropbox_module import upload
from pre_processing import pre_processing
from get_tags_tf import get_tags_tf
# Custom Modules
from sonar_module import sound_sensor
from vision_module import get_tags
import api


# from clarifai_module import get_tags


class Pi:
    def __init__(self):
        # self.app = ClarifaiApp(api_key='c0c92d06f75d4ed5a067630dafface26') #clarifai API
        self.dbx = Dropbox('CYUdRtzfjvAAAAAAAAAAFwaSXZUo4_2S_-jWgKO7wf3Gkd9OrdiL67hf97oHTJ3I')  # Dropbox
        # self.model = self.app.models.get('general-v1.3') #Use Custom Model?
        self.visionClient = vision.ImageAnnotatorClient()

        # GPIO for SONAR Sensor
        gp.setmode(gp.BCM)
        gp.setup(23, gp.OUT)
        gp.setup(24, gp.IN)
        gp.setwarnings(False)

        try:
            with open('config.json', 'r') as json_config_file:
                config = json.loads(json_config_file.read())

            for k, v in config.iteritems():
                os.environ[k] = v
            print os.environ['CHARTS_DB_HOST']
        # Config file not passed! Using defaults in local
        except Exception as e:
            print e
            logging.warning('Config file not found. Using defaults with CHARTS_DB_HOST as %s' % (
                os.environ.get('CHARTS_DB_HOST', None)))

    # Config Files

    # Main Loop, iterated every 15 seconds

    def loop(self):

        # self.config_dict = load(open('config.p', 'rb'))
        self.config_dict = dict()
        self.init_dist = sound_sensor()
        print self.init_dist
        self.U_ID = str(get_mac())
        self.config_dict.update({"U_ID": self.U_ID})
        self.config_dict.update({"DEPTH": self.init_dist})

        while api.confirm_authentication(self.U_ID):
            print "L"
            pass

        lat, lon = api.get_location(self.U_ID)
        self.config_dict["LAT"], self.config_dict["LONG"] = lat, lon
        self.config_dict["USER_NAME"] = str(api.get_username(self.U_ID))
        self.config_dict["TYPE"] = api.get_type(self.U_ID)
        dump(self.config_dict, open('config.p', 'wb'))
        # Dict_to_API used to send API requests
        self.dict_to_API = dict()
        self.dict_to_API.update({"U_ID": self.config_dict["U_ID"]})
        self.dict_to_API.update({"LAT": self.config_dict["LAT"]})
        self.dict_to_API.update({"LONG": self.config_dict["LONG"]})
        self.dict_to_API.update({"USER_NAME": self.config_dict["USER_NAME"]})
        self.dict_to_API.update({"TYPE": self.config_dict["TYPE"]})

        i = 0
        while True:
            print "Recording Distance"
            dist = sound_sensor()
            if int(dist) > self.config_dict['DEPTH']+1:
                sleep(5)
                continue
            image_name = self.dict_to_API["U_ID"] + "_" + str(datetime.datetime.now()) + '.jpg'
            print "Capturing Image"
            os.system("fswebcam -r 1024x768 -S 30 --no-banner -q image_{}.jpg".format(i))

            print "Sleeping for 5 seconds"
            sleep(5)  # Maybe 30 secs? CHANGE TO 15 for review

            self.dict_to_API.update({"LEVEL": int(self.config_dict['DEPTH'] - dist)})
            self.dict_to_API.update({"TIMESTAMP": str(datetime.datetime.now())})

            print "Getting Tags (Experimental)"
            # tags = get_tags(ClImage, self.model, 'image.jpg') THIS WAS CLARIFAI
            if not pre_processing("image_{}.jpg".format(i), "image_{}.jpg".format((i+1)%2)):
                tags = get_tags(self.visionClient, types, 'send_to_vision.jpg')
                # tags = get_tags_tf('image_{}.jpg'.format(i))
                self.dict_to_API.update({"TAGS": tags})

                print "Uploading Image"
                DROPBOX_URL = upload(self.dbx, "image_{}.jpg".format(i), image_name)
                self.dict_to_API.update({"URL": DROPBOX_URL})

                # print "Distance: {} cms".format(dist)
                # print "Dropbox URL: {}".format(DROPBOX_URL)
                print self.dict_to_API
                print ""
                print ""
                i = (i + 1) % 2
                api.send_data(json.dumps(self.dict_to_API))
            else:
                print "Same images, no new waste."
