#!/usr/bin/env python
import cv
from cv2 import *
import numpy as np

class Point:
 def __init__(self, requiredheight, requiredwidth, requiredactive):
        self.height = requiredheight
        self.width = requiredwidth
        self.isActive = requiredactive

#namedWindow("Normal feed", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Edge detection", cv.CV_WINDOW_AUTOSIZE)
cam = VideoCapture(0)

# Keep hands points
leftHand = Point(0,0,False)
rightHand = Point(0,0,False)

while True:
 s, image = cam.read()
 if s:
  imwrite('cam_image.jpg', image)

 # Initialise
 leftHand.isActive = False
 rightHand.isActive = False

 # Code from stack overflow
 # Open the image
 image = cv.LoadImage('cam_image.jpg') 

 yuv = cv.CreateImage(cv.GetSize(image),8,3)
	
 # convert to grey
 gray = cv.CreateImage(cv.GetSize(image),8,1)
 cv.CvtColor(image,yuv, cv.CV_BGR2YCrCb)
 cv.Split(yuv,gray, None,None,None)

 canny = cv.CreateImage(cv.GetSize(image),8,1)
 cv.Canny(gray,canny,50,200)

 # Search for dots
 for x in range(0, image.height):
  for y in range(0, image.width):
	# get the value of the current pixel
	pixel = canny[x, y]

	# If white check in which quarter is located
	if pixel == 255.0:
	 # If left quarter and not read yet, store coordinates.
	 if y < image.width/4 and not rightHand.isActive:
	  rightHand.height = x
	  rightHand.width = y
	  rightHand.isActive = True
	 # If right quarter and not read yet, store coordinates.
	 elif y > image.width*3/4 and not leftHand.isActive:
	  leftHand.height = x
	  leftHand.width = y
	  leftHand.isActive = True
	 # If both hands have been read, stop the loops.
	 elif rightHand.isActive and leftHand.isActive:
	  break

 # For testing: draw circles in the original image.
 cv.Circle(image,(rightHand.height,rightHand.width), 2,cv.RGB(255,0,0))
 cv.Circle(image,(leftHand.height,leftHand.width), 2,cv.RGB(0,255,0))

 # Check where are the dots and print the resulting command.
 if rightHand.height < image.height/2:
  if leftHand.height < image.height/2:
	print "Both up"
  else:
	print "Right up"
 else:
  if leftHand.height < image.height/2:
	print "Left up"
  else:
	print "Both down"

 #Show the images
 #cv.ShowImage("Normal feed", image)
 cv.ShowImage("Edge detection", canny)	
 waitKey(1)	
	