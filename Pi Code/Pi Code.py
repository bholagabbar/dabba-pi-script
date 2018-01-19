import logging, time, smtplib
import RPi.GPIO as gp
import os
import requests
import json
from dropbox import Dropbox
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from time import sleep
from pickle import load, dump
from datetime.datetime import now
from uuid import getnode as get_mac

#Custom Modules

import telegram_api
from sonar_module import sound_sensor
from dropbox_module import upload
from clarifai_module import get_tags


if __name__ == '__main__':
	app = ClarifaiApp(api_key='c0c92d06f75d4ed5a067630dafface26') #clarifai API
	dbx = dropbox('CYUdRtzfjvAAAAAAAAAAFwaSXZUo4_2S_-jWgKO7wf3Gkd9OrdiL67hf97oHTJ3I') #Dropbox
	model = app.models.get('general-v1.3') #Use Custom Model?

	#GPIO for SONAR Sensor
	gp.setmode(gp.BCM)
	gp.setup(23, gp.OUT)
	gp.setup(24, gp.IN)
	gp.setwarnings(False)

	#Config Files
	if os.path.isfile('config.p'):
		config_dict = load(open('config.p', 'rb'))
	else:
		init_dist = sound_sensor(time)
		location_lat, location_long = get_location()
		config_dict = dict()
		U_ID = get_mac()
		config_dict.update({"DEPTH":init_dist})
		config_dict.update({"LAT":location_lat})
		config_dict.update({"LONG":location_long})
		dump(config_dict, open('config.p', 'wb'))

	#Logging purposes
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

	#Dict_to_API used to send API requests
	dict_to_API = dict()
	dict_to_API.update({"U_ID":config_dict["U_ID"]})
	dict_to_API.update({"LAT":config_dict["LAT"]})
	dict_to_API.update({"LONG":config_dict["LONG"]})
	
	#Main Loop, iterated every 15 seconds
	while True:

		dist = sound_sensor(time)
		image_name = dict_to_API["U_ID"] + "_" + str(now()) + '.jpg'
		
		os.system("fswebcam -S 30 --no-banner image.jpg")
		sleep(5) #Maybe 30 secs? CHANGE TO 15 for review
		
		dict_to_API.update({"LEVEL":config_dict['DEPTH'] - dist})
		dict_to_API.update({"TIMESTAMP":str(now())})
		
		tags = get_tags(ClImage, model, 'image.jpg')
		dict_to_API.update({"TAGS:"tags})

		DROPBOX_URL = upload(dbx, "image.jpg", image_name)
		dict_to_API.update({"URL":DROPBOX_URL})

		# api.send_data(dict_to_API)
