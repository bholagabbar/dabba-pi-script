def upload(dbx, URL, image_name):
	dbx.files_upload(open(url, 'rb').read(), '/'+image_name)
	return str(dbx.sharing_create_shared_link().url)
