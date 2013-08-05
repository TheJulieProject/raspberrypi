#!/usr/bin/env python
from cv2 import *

# Open the webcam
cam= VideoCapture(0)

# View for the final image
namedWindow("Webcam feed", cv.CV_WINDOW_AUTOSIZE)

while True:
	# grab an image from the camera
    s, image = cam.read()
    if s:
		# *** USER: change name of file
		imwrite('cam_image.jpg', image)

    my_image = imread('cam_image.jpg')
    	
	# display the image on the screen
	imshow("Webcam feed", my_image)
	waitKey(1)
