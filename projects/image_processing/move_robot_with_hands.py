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

# Window for the final image
namedWindow("Edge detection", cv.CV_WINDOW_AUTOSIZE)

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

 # Check where the dots are and print the resulting command.
 if rightHand.height < image.height/3:
  if leftHand.height < image.height/3:
	print "Forward"
  elif leftHand.height < image.height*2/3:
	print "Forward_right"
  else:
	print "Turn_left"
 elif rightHand.height < image.height*2/3:
  if leftHand.height < image.height/3:
	print "Forward_left"
  elif leftHand.height < image.height*2/3:
	print "Stop"
  else:
	print "Back_right"
 else:
  if leftHand.height < image.height/3:
	print "Turn_right"
  elif leftHand.height < image.height*2/3:
	print "Back_left"
  else:
	print "Back"

 #Show the image
 cv.ShowImage("Edge detection", canny)	
 waitKey(1)	
	