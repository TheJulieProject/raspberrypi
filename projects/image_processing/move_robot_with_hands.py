#!/usr/bin/env python
import cv
from cv2 import *
import numpy as np

# Represent a point with the x (width) and y (height) coordinates and if it 
# is active or not.
class Point:
 def __init__(self, requiredheight, requiredwidth, requiredactive):
        self.height = requiredheight
        self.width = requiredwidth
        self.isActive = requiredactive
	self.currentState = 0
	self.previousState = 0

# Window for the final image
namedWindow("Robot movement", cv.CV_WINDOW_AUTOSIZE)

# Set webcam
cam = VideoCapture(0)

# Keep hands points
leftHand = Point(0,0,False)
rightHand = Point(0,0,False)

while True:
 # Take an image and save it
 s, image = cam.read()
 if s:
  imwrite('cam_image.jpg', image)

 # Initialise hand points
 leftHand.isActive = False
 rightHand.isActive = False

 # Code from stack overflow
 # Open the image
 image = cv.LoadImage('cam_image.jpg') 

 yuv = cv.CreateImage(cv.GetSize(image),8,3)
	
 # convert image to grey
 gray = cv.CreateImage(cv.GetSize(image),8,1)
 cv.CvtColor(image,yuv, cv.CV_BGR2YCrCb)
 cv.Split(yuv,gray, None,None,None)

 # Use canny algorithm for edge detection
 canny = cv.CreateImage(cv.GetSize(image),8,1)
 cv.Canny(gray,canny,50,200)

 # Search for hands
 for x in range(0, image.height):
  for y in range(0, image.width):
	# get the value of the current pixel
	pixel = canny[x, y]

	# If white check in which quarter is located
	if pixel == 255.0:
	 # If left quarter and not read yet, store state.
	 if y < image.width/4 and not rightHand.isActive:
	  if x < image.height/3:
		rightHand.currentState = 1
		rightHand.isActive = True
	  elif x > image.height*2/3:
		rightHand.currentState = -1
		rightHand.isActive = True
	  else:
		rightHand.currentState = 0
		rightHand.isActive = True
	 # If right quarter and not read yet, store state.
	 if y > image.width*3/4 and not leftHand.isActive:
	  if x < image.height/3:
		leftHand.currentState = 1
		leftHand.isActive = True
	  elif x > image.height*2/3:
		leftHand.currentState = -1
		leftHand.isActive = True
	  else:
		leftHand.currentState = 0
		leftHand.isActive = True
	 # If both hands have been read, stop the loops.
	 if rightHand.isActive and leftHand.isActive:
	  break 

 # Send a message if the current state is different to the previous state.
 if rightHand.currentState != rightHand.previousState:
  if rightHand.currentState == 1:
	print "Right up"
  elif rightHand.currentState == -1:
	print "Right down"
  else:
	print "Stop right"

  rightHand.previousState = rightHand.currentState

 elif leftHand.currentState != leftHand.previousState:
  if leftHand.currentState == 1:
	print "Left up"
  elif leftHand.currentState == -1:
	print "Left down"
  else:
	print "Stop Left"

  leftHand.previousState = leftHand.currentState
 
 #Show the image
 cv.ShowImage("Robot movement", canny)	
 waitKey(1)	
	