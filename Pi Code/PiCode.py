import RPi.GPIO as gp
import os
import requests
import json
import datetime
from dropbox import Dropbox
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from time import sleep
from pickle import load, dump
from uuid import getnode as get_mac
from multiprocessing import Process

#Custom Modules

import telegram_api
from sonar_module import sound_sensor
from dropbox_module import upload
from clarifai_module import get_tags


class Pi:
	def __init__ (self):
		self.app = ClarifaiApp(api_key='c0c92d06f75d4ed5a067630dafface26') #clarifai API
		self.dbx = Dropbox('CYUdRtzfjvAAAAAAAAAAFwaSXZUo4_2S_-jWgKO7wf3Gkd9OrdiL67hf97oHTJ3I') #Dropbox
		self.model = self.app.models.get('general-v1.3') #Use Custom Model?

	#GPIO for SONAR Sensor
		gp.setmode(gp.BCM)
		gp.setup(23, gp.OUT)
		gp.setup(24, gp.IN)
		gp.setwarnings(False)

	#Config Files
		while not os.path.isfile('config.p'):
			continue

		sleep(5)
		self.config_dict = load(open('config.p', 'rb'))
	
		self.init_dist = sound_sensor()
		self.U_ID = str(get_mac())
		self.config_dict.update({"U_ID":self.U_ID})
		self.config_dict.update({"DEPTH":self.init_dist})
		dump(self.config_dict, open('config.p', 'wb'))

		#Dict_to_API used to send API requests
		self.dict_to_API = dict()
		self.dict_to_API.update({"U_ID":self.config_dict["U_ID"]})
		self.dict_to_API.update({"LAT":self.config_dict["LAT"]})
		self.dict_to_API.update({"LONG":self.config_dict["LONG"]})
		
	#Main Loop, iterated every 15 seconds

	def loop(self):
		while True:

			dist = sound_sensor()
			image_name = self.dict_to_API["U_ID"] + "_" + str(datetime.datetime.now()) + '.jpg'
		
			os.system("fswebcam -S 30 --no-banner image.jpg")
			sleep(5) #Maybe 30 secs? CHANGE TO 15 for review
			
			self.dict_to_API.update({"LEVEL":self.config_dict['DEPTH'] - dist})
			self.dict_to_API.update({"TIMESTAMP":str(datetime.datetime.now())})
			
			tags = get_tags(ClImage, self.model, 'image.jpg')
			self.dict_to_API.update({"TAGS":tags})

			DROPBOX_URL = upload(self.dbx, "image.jpg", image_name)
			self.dict_to_API.update({"URL":DROPBOX_URL})

			# api.send_data(self.dict_to_API)
