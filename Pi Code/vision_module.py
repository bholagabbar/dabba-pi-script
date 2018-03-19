def get_tags(client, types, image):

	# Loads the image into memory
	with io.open(image, 'rb') as image_file:
	    content = image_file.read()

	image = types.Image(content=content)

	response = client.label_detection(image=image)
	labels = response.label_annotations
	return labels