import logging, time, smtplib
import RPi.GPIO as gp
import os
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

THRESHOLD = 5 #5cms from sensor is when the bin is full
### Sensor on PIN 23 & 24

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

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

	while True:
		dist = soundSensor()
		os.system("fswebcam -S 30 image.jpg")
		'''CLarifai in the following lines'''
		#image = ClImage(file_obj=open('image.jpg', 'rb'))
		#tags = model.predict([image])
		#API call goes here