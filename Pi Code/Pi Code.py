import logging, time, smtplib
import RPi.GPIO as gp
import os
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from time import sleep
from pickle import load, dump
from datetime.datetime import now

### Sensor on PIN 23 & 24

gp.setmode(gp.BCM)
gp.setup(23, gp.OUT)
gp.setup(24, gp.IN)

def soundSensor():
	while True:
		gp.output(23, True)
		time.sleep(0.00001)
		gp.output(23, False)

		while gp.input(24) == 0:
			pulseStart = time.time()

		while gp.input(24) == 1:
			pulseEnd = time.time()

		pulseDur = pulseEnd - pulseStart
		dist = pulseDur * 17150
		dist = round(dist, 2)
		# print dist
		return dist

if __name__ == '__main__':
	app = ClarifaiApp(api_key='c0c92d06f75d4ed5a067630dafface26')
	model = app.models.get('general-v1.3') #Use Custom Model?
	gp.setmode(gp.BCM)
	gp.setup(21, gp.OUT)
	gp.setup(16, gp.OUT)
	gp.setup(13, gp.OUT)
	gp.setup(6, gp.OUT)
	gp.setup(23, gp.OUT)
	gp.setup(24, gp.IN)
	gp.setwarnings(False)

	if os.path.isfile('config.p'):
		config_dict = load(open('config.p', 'rb'))
	else:
		init_dist = soundSensor()
		#location_lat, location_long = get_location()
		config_dict = dict()
		U_ID = api.getID() #bholagabbar
		config_dict.update({"DEPTH":init_dist})
		config_dict.update({"LAT":location_lat})
		config_dict.update({"LONG":location_long})
		dump(open('config.p', 'wb'), config_dict)

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
	
	dict_to_API = dict()
	dict_to_API.update({"U_ID":config_dict["U_ID"]}) #dynamic ID or sth
	while True:

		dist = soundSensor()
		os.system("fswebcam -S 30 --no-banner image.jpg")
		sleep(5) #Maybe 30 secs?
		dict_to_API.update({"LEVEL":config_dict['DEPTH'] - dist})
		dict_to_API.update({"TIMESTAMP":str(now())})
		
		'''CLarifai in the following lines'''
		#image = ClImage(file_obj=open('image.jpg', 'rb'))
		#tags = model.predict([image])
		#add tags to dict_to_API
		#dropbox integration
		api.send_data(dict_to_API)
