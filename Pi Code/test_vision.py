from google.cloud import vision
from google.cloud.vision import types

def get_tags(client, types, image):
    # Loads the image into memory
    with io.open(image, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    temp = []
    for label in labels:
        if label.score > 0.5:
            temp.append(label.description)
    return temp

if __name__ == '__main__':
    visionClient = vision.ImageAnnotatorClient()
    print get_tags(visionClient, types, image)