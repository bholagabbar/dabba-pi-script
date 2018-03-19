import RPi.GPIO as gp
import os
import requests
import json
import datetime
import io
from dropbox import Dropbox
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from time import sleep
from pickle import load, dump
from uuid import getnode as get_mac
from multiprocessing import Process
from google.cloud import vision
from google.cloud.vision import types


#Custom Modules
from sonar_module import sound_sensor
from dropbox_module import upload
from vision_module import get_tags
# from clarifai_module import get_tags



class Pi:
	def __init__ (self):
		# self.app = ClarifaiApp(api_key='c0c92d06f75d4ed5a067630dafface26') #clarifai API
		self.dbx = Dropbox('CYUdRtzfjvAAAAAAAAAAFwaSXZUo4_2S_-jWgKO7wf3Gkd9OrdiL67hf97oHTJ3I') #Dropbox
		# self.model = self.app.models.get('general-v1.3') #Use Custom Model?
		self.visionClient = vision.ImageAnnotatorClient()

	#GPIO for SONAR Sensor
		gp.setmode(gp.BCM)
		gp.setup(23, gp.OUT)
		gp.setup(24, gp.IN)
		gp.setwarnings(False)

	#Config Files

		
	#Main Loop, iterated every 15 seconds

	def loop(self):
		flag = False
		while not True: ##CHANGE THIS. Add api.checkAuthentication(str(get_mac()))
			if not flag:
				print "Please configure before using."
				flag = True
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
		
		while True:
			print "Recording Distance"
			dist = sound_sensor()
			image_name = self.dict_to_API["U_ID"] + "_" + str(datetime.datetime.now()) + '.jpg'
			print "Capturing Image"
			os.system("fswebcam -S 30 --no-banner -q image.jpg")

			print "Sleeping for 5 seconds"
			sleep(5) #Maybe 30 secs? CHANGE TO 15 for review
			
			self.dict_to_API.update({"LEVEL":self.config_dict['DEPTH'] - dist})
			self.dict_to_API.update({"TIMESTAMP":str(datetime.datetime.now())})
			
			print "Getting Tags (Experimantal)"			
			# tags = get_tags(ClImage, self.model, 'image.jpg') THIS WAS CLARIFAI
			tags = get_tags(self.visionClient, types, 'image.jpg')
			self.dict_to_API.update({"TAGS":tags})

			print "Uploading Image"
			DROPBOX_URL = upload(self.dbx, "image.jpg", image_name)
			self.dict_to_API.update({"URL":DROPBOX_URL})

			# print "Distance: {} cms".format(dist)
			# print "Dropbox URL: {}".format(DROPBOX_URL)
			print self.dict_to_API
			print ""
			print ""

			# api.send_data(self.dict_to_API)
