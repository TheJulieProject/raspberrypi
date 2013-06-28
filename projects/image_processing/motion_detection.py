#!/usr/bin/env python
import cv
from cv2 import *
import math
   
# Set the camera
cam = VideoCapture(0)

# Read first image and save it
s, image = cam.read()
if s:
 imwrite('motion1.jpg', image)

while True:
	# Open the image 
	image = cv.LoadImage('cam_image.jpg',cv.CV_LOAD_IMAGE_GRAYSCALE)
	
	# Show the image
	cv.ShowImage("Motion", dstSobel)	
	waitKey(0)	

	
