import cv2
import numpy as np

# image2 -> the image of the dustbin before throwing in the new garbage(object of interest)
# image1 -> the image of the dustbin after throwing in the new garbage(object of interest)
# plz click images from a steady camera, else the algo wont work

def pre_processing(newImg, prevImg):
    try:
        image1 = cv2.imread(newImg)
        #image1 = cv2.resize(image1,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
        # image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Draw01',image1)

        image2 = cv2.imread(prevImg)
        #image2 = cv2.resize(image2,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
        # image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Draw02',image2)


        # image3 = cv2.subtract(image1, image2)
        # cv2.imshow('Draw03',image3)

        # (T, threshImage) = cv2.threshold(image3, 1, 255, cv2.THRESH_BINARY)
        # cv2.imshow('Draw04',threshImage)
        # cv2.imwrite('threshImage.jpg',threshImage)

        # clrimg = cv2.imread(newImg)
        # abc = cv2.bitwise_and(clrimg, clrimg, mask = cv2.imread('threshImage.jpg', 0))
        # cv2.imwrite('send_to_vision.jpg',abc)
        diff = cv2.absdiff(image1, image2)
        imask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        thr = 1
        imask = imask > thr

        canvas = np.zeros_like(image1, np.uint8)
        canvas[imask] = image1[imask]
        cv2.imwrite("send_to_vision.jpg", canvas)
    except Exception as e:
	print "LOL ho gaya"
	print e
        newImg = cv2.imread(newImg)
        cv2.imwrite('send_to_vision.jpg', newImg)
#cv2.Copy(clrimg, clrimg, threshImage)

# cv2.imshow('Draw05',abc)

# cv2.waitKey(0)
