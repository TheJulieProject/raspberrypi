#!/usr/bin/env python
import cv
from cv2 import *
import math

# Represent a point with the x (width) and y (height) coordinates and if it 
# is active or not.
class Point:
 def __init__(self, requiredheight, requiredwidth, requiredactive):
 	self.height = requiredheight
	self.width = requiredwidth
	self.isActive = requiredactive
 
# Get the corners of the octagon and draw them in the screen
def octagon(img): 
  # Import
  global point1, point2, point3, point4, point5, point6, point7, point8, t

  # Calculate the smallest of the image parameters
  if img.height < img.width:
   smallest = img.height
  else:
   smallest = img.width

  # Distance from borders (in pixels)
  t = 13

  # Value to center the octagon (in pixels)
  c = 20

  # Calculate distance d from a corner to the centre of the square.
  d = int((smallest / 2 - t) * math.sqrt(2))

  # Set points as tuples and draw them as green circles.
  point1 = Point(smallest-t-d + c,t, False)
  cv.Circle(imcolor,(point1.height, point1.width),radius,cv.RGB(0, 255, 0))

  point2 = Point(t+d+ c, t, False)
  cv.Circle(imcolor,(point2.height, point2.width),radius,cv.RGB(0, 255, 0))

  point3 = Point(smallest - t+ c, smallest-t-d, False)
  cv.Circle(imcolor,(point3.height, point3.width),radius,cv.RGB(0, 255, 0))

  point4 = Point(smallest - t+ c, t+d, False)
  cv.Circle(imcolor,(point4.height, point4.width),radius,cv.RGB(0, 255, 0))

  point5 = Point(t+d+ c,smallest - t, False)
  cv.Circle(imcolor,(point5.height, point5.width),radius,cv.RGB(0, 255, 0))

  point6 = Point(smallest-t-d+ c, smallest - t, False)
  cv.Circle(imcolor,(point6.height, point6.width),radius,cv.RGB(0, 255, 0))

  point7 = Point(t+ c, t+d, False)
  cv.Circle(imcolor,(point7.height, point7.width),radius,cv.RGB(0, 255, 0))

  point8 = Point(t+ c, smallest-t-d, False)
  cv.Circle(imcolor,(point8.height, point8.width),radius,cv.RGB(0, 255, 0))

  # Show the image before using the harris algorithm
  cv.ShowImage("Octagon", imcolor)

# Check if a corner is in one of the 8 regions and, in that case, activate it.
def active(x,y): 
 if not point1.isActive and math.fabs(x-point1.height) < radius and math.fabs(y - point1.width) < radius:
  point1.isActive = True
 elif not point2.isActive and math.fabs(x-point2.height) < radius and math.fabs(y - point2.width) < radius:
  point2.isActive = True
 elif not point3.isActive and math.fabs(x-point3.height) < radius and math.fabs(y - point3.width) < radius:
  point3.isActive = True
 elif not point4.isActive and math.fabs(x-point4.height) < radius and math.fabs(y - point4.width) < radius:
  point4.isActive = True
 elif not point5.isActive and math.fabs(x-point5.height) < radius and math.fabs(y - point5.width) < radius:
  point5.isActive = True
 elif not point6.isActive and math.fabs(x-point6.height) < radius and math.fabs(y - point6.width) < radius:
  point6.isActive = True
 elif not point7.isActive and math.fabs(x-point7.height) < radius and math.fabs(y - point7.width) < radius:
  point7.isActive = True
 elif not point8.isActive and math.fabs(x-point8.height) < radius and math.fabs(y - point8.width) < radius:
  point8.isActive = True

# Change from green to blue the points that are active.
def bluePoint():
 if point1.isActive:
    cv.Circle(imcolor,(point1.height, point1.width),radius,cv.RGB(0, 0, 255))
 if point2.isActive:
    cv.Circle(imcolor,(point2.height, point2.width),radius,cv.RGB(0, 0, 255))
 if point3.isActive:
    cv.Circle(imcolor,(point3.height, point3.width),radius,cv.RGB(0, 0, 255))
 if point4.isActive:
    cv.Circle(imcolor,(point4.height, point4.width),radius,cv.RGB(0, 0, 255))
 if point5.isActive:
    cv.Circle(imcolor,(point5.height, point5.width),radius,cv.RGB(0, 0, 255))
 if point6.isActive:
    cv.Circle(imcolor,(point6.height, point6.width),radius,cv.RGB(0, 0, 255))
 if point7.isActive:
    cv.Circle(imcolor,(point7.height, point7.width),radius,cv.RGB(0, 0, 255))
 if point8.isActive:
    cv.Circle(imcolor,(point8.height, point8.width),radius,cv.RGB(0, 0, 255))

# Check which points are not activated and return the resulting direction
def direction():
 if not point1.isActive:
  if not point4.isActive and point2.isActive and point3.isActive  and point5.isActive  and point6.isActive  and point7.isActive  and point8.isActive:
	return "Right_Back"
  elif not point6.isActive and point2.isActive and point3.isActive  and point5.isActive  and point4.isActive  and point7.isActive  and point8.isActive:
	return "Left_Turn"
 elif not point2.isActive:
  if not point5.isActive and point1.isActive and point3.isActive  and point4.isActive  and point6.isActive  and point7.isActive  and point8.isActive:
	return "Right_Turn"
  elif not point7.isActive and point1.isActive and point3.isActive  and point4.isActive  and point6.isActive  and point5.isActive  and point8.isActive:
	return "Left_Back"
 elif not point3.isActive:
  if not point6.isActive and point1.isActive and point2.isActive  and point4.isActive  and point5.isActive  and point7.isActive  and point8.isActive:
	return "Right_Forw"
  elif not point8.isActive and point1.isActive and point2.isActive  and point4.isActive  and point5.isActive  and point6.isActive  and point7.isActive:
	return "Back"
 elif not point4.isActive:
  if not point7.isActive and point2.isActive and point3.isActive  and point5.isActive  and point6.isActive  and point1.isActive  and point8.isActive:
	return "Forw"
 elif not point5.isActive:
  if not point8.isActive  and point1.isActive and point2.isActive  and point3.isActive  and point4.isActive  and point6.isActive  and point7.isActive:
	return "Left_Forw" 
   
# ------------------------- START -------------------

# Keep octogone points.
global point1, point2, point3, point4, point5, point6, point7, point8

# Radius for circles
global radius
radius = 7

# Create the windows to show the final result and the intermediate steps.
namedWindow("Normal feed", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Black and white", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Octagon", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Final output", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Red channel", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Green channel", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Blue channel", cv.CV_WINDOW_AUTOSIZE)

# Set the webcam
cam = VideoCapture(0)

while True:
	# Read and image and save it
	s, image = cam.read()
	if s:
	 imwrite('cam_image.jpg', image)

	# Code from Glowing python.
	# Load image in colour, in grey scale and using the cv2 command.
	imcolor = cv.LoadImage('cam_image.jpg')
	image = cv.LoadImage('cam_image.jpg',cv.CV_LOAD_IMAGE_GRAYSCALE)
	imgchannels = imread('cam_image.jpg')

	# Separe variables for separate red, green and blue channels.
	channelR = split(imgchannels)[2]
	channelG = split(imgchannels)[1]
	channelB = split(imgchannels)[0]

	# Show the channels.
	imshow("Red channel", channelR)
	imshow("Green channel", channelG)
	imshow("Blue channel", channelB)

	# Show image in black and white and in colour.
	cv.ShowImage("Normal feed", imcolor)
	cv.ShowImage("Black and white", image)

	# Initialise the octagon
	octagon(imcolor)	
	
	# Destination of the harris algorithm
	cornerMap = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
	
	# OpenCV corner detection
	cv.CornerHarris(image,cornerMap,3)
	
	# Iterate through each pixel to get the final command.
	for y in range(0, image.height):
 	 for x in range(0, image.width):
	  harris = cv.Get2D(cornerMap, y, x) # get the x,y value
 	  
	  # check the corner detector response
	  if harris[0] > 10e-06:
 	  
	   # draw a small circle on the original image to represent the corner
           cv.Circle(imcolor,(x,y),2,cv.RGB(155, 0, 25))

	   # Check if it is in one of the 8 points.
	   active(x,y)

	   # Change to blue the activated corners of the octagon.
	   bluePoint()	

	   # Print the resulting direction
	   direct = direction()
	   if not direct == None:
		print direct	

	# Show the final result.
	cv.ShowImage("Final output", imcolor)	
	waitKey(1)	
	