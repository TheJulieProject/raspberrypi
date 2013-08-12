#!/usr/bin/env python
'''
This program takes an image and resizes it by a factor of 2. Both odf them
are showed on the screen.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
import cv
from cv2 import *

# Create windows to display the original image and the one with double size.
# *** USER: change the name of the windows that show the video.
namedWindow("Doubled")
namedWindow("Normal", cv.CV_WINDOW_AUTOSIZE)

# Set the camera
cam = VideoCapture(0)

while True:
	# Read an image adn save it
	s, image = cam.read()
	if s:
		# *** USER: change the name of file
		imwrite('cam_image.jpg', image)

	# read the image
	image = cv.LoadImageM('cam_image.jpg')

	# Create a matrix with double the size of the original image and 8-bits
	# *** USER: change the factor which resizes de image.
	doubleimg = cv.CreateMat(image.rows * 2, image.cols * 2, cv.CV_8UC3)

	# Change the size of the image
	cv.Resize(image, doubleimg)	

	# *** USER: Save the image if you want
	cv.SaveImage("double_image.jpg",doubleimg)
	
	# Show images
	cv.ShowImage("Normal", image)
	cv.ShowImage("Doubled", doubleimg)	
	waitKey(1)
