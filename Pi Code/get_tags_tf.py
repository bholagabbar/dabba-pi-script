import cv2
import requests
import json

def get_tags_tf(image_path):
	url = 'http://192.168.2.1:5000/predict'
	img = cv2.imread(image_path)
	_, image_encoded = cv2.imencode('.jpg',img)
	data = image_encoded.tostring()
	r = requests.post(url, data)
	tags = json.loads(r.text)['output']
	return tags
