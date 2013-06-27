#!/usr/bin/env python
#from imgproc import *
import cv
from cv2 import *
import math

class Point:
 def __init__(self, requiredheight, requiredwidth, requiredactive):
 	self.height = requiredheight
	self.width = requiredwidth
	self.isActive = requiredactive
 
   
# ------------------------- START -------------------

#namedWindow("Sobel", cv.CV_WINDOW_AUTOSIZE)
cam = VideoCapture(0)

s, image = cam.read()
if s:
 imwrite('cam_image.jpg', image)

# Open the image 
#imcolor = cv.LoadImage('cam_image.jpg')
image = cv.LoadImage('cam_image.jpg',cv.CV_LOAD_IMAGE_GRAYSCALE)

# Code from glowing python
dstSobel = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
cv.Sobel(image, dstSobel, 1, 1, 3)	
	
# Show the image
#cv.ShowImage("Sobel", dstSobel)	
#waitKey()	

# Save the image for testing
cv.SaveImage('sobel.jpg', dstSobel)
	