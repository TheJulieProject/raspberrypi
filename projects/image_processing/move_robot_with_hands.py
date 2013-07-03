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

# Window for the final image and the normal one
namedWindow("Normal feed", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Robot movement", cv.CV_WINDOW_AUTOSIZE)

# Set webcam
cam = VideoCapture(2)

# Keep hands points
leftHand = Point(0,0,False)
rightHand = Point(0,0,False)

def move():
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
 
 # Draw guide lines in the image.
 cv.Line(image, (image.width/4, 0), (image.width/4, image.height/3), cv.RGB(255,0, 0)) 
 cv.Line(image, (0, image.height/3), (image.width/4, image.height/3), cv.RGB(255,0, 0))
 
 cv.Line(image, (image.width*3/4, 0), (image.width*3/4, image.height/3), cv.RGB(255,0, 0)) 
 cv.Line(image, (image.width*3/4, image.height/3), (image.width, image.height/3), cv.RGB(255,0, 0)) 

 cv.Line(image, (image.width/4, image.height*2/3), (image.width/4, image.height), cv.RGB(255,0, 0)) 
 cv.Line(image, (0, image.height*2/3), (image.width/4, image.height*2/3), cv.RGB(255,0, 0)) 

 cv.Line(image, (image.width*3/4, image.height*2/3), (image.width*3/4, image.height), cv.RGB(255,0, 0)) 
 cv.Line(image, (image.width*3/4, image.height*2/3), (image.width, image.height*2/3), cv.RGB(255,0, 0)) 

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

 # If at the end of the loop one of the hands hasnt been read, 
 # it current coordinate will change to 0.
 if not rightHand.isActive:
  rightHand.currentState = 0
 if not leftHand.isActive:
  leftHand.currentState = 0

 # Keep commands
 commandLeft = commandRight = ""

 # Send a message if the current state is different to the previous state.
 if rightHand.currentState != rightHand.previousState:
  if rightHand.currentState == 1:
	commandRight = "1"
  elif rightHand.currentState == -1:
	commandRight = "-1"
  else:
	commandRight = "0"

  rightHand.previousState = rightHand.currentState

 else:
	commandRight = "Do nothing"

 if leftHand.currentState != leftHand.previousState:
  if leftHand.currentState == 1:
	commandLeft = "1"
  elif leftHand.currentState == -1:
	commandLeft = "-1"
  else:
	commandLeft = "0"

  leftHand.previousState = leftHand.currentState

 else:
	commandLeft = "Do nothing"
 
 #Show the image
 cv.ShowImage("Normal feed", image)
 cv.ShowImage("Robot movement", canny)	
 waitKey(1)	

 # Return the command
 return commandRight + "_" + commandLeft
	
#while True:
 #move()