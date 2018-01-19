def get_tags(ClImahe, model, url):
	image = ClImage(file_obj=open(url, 'rb'))
	tags = model.predict([image])
	#some post processing
	return 0