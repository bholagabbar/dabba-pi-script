def upload(dbx, url, image_name):
	dbx.files_upload(open(url, 'rb').read(), '/'+image_name)
	return str(dbx.sharing_create_shared_link('/'+image_name).url)
