#!/usr/bin/env python
#from imgproc import *
import cv
from cv2 import *

namedWindow("Doubled")
namedWindow("Normal", cv.CV_WINDOW_AUTOSIZE)
cam = VideoCapture(0)

while True:

	s, image = cam.read()
	if s:
	 imwrite('cam_image.jpg', image)

	image = cv.LoadImageM('cam_image.jpg')
	doubleimg = cv.CreateMat(image.rows * 2, image.cols * 2, cv.CV_8UC3)

	cv.Resize(image, doubleimg)	
	
	# Show the image
	cv.ShowImage("Normal", image)
	cv.ShowImage("Doubled", doubleimg)	
	waitKey(1)

	# testing
	#print "testing"	
