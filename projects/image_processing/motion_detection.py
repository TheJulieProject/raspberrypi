#!/usr/bin/env python
import cv
from cv2 import *
import math
   
# Set the camera
cam = VideoCapture(0)

# Keep number of different pixels
differentPixels  = 0

# Read first image and save it
s, image = cam.read()
if s:
 imwrite('motion1.jpg', image)

while True:
	# Initialise pixel count
	differentPixels = 0

	# Open previous image 
	prevImage = cv.LoadImage('motion1.jpg')

	# Take another image
	s, image = cam.read()
	if s:
	 imwrite('motion2.jpg', image)

	# Read it
	image = cv.LoadImage('motion2.jpg')

	# Iterate through each pixel comparing the ones of both images.
	for y in range(0, image.height):
         for x in range(0, image.width):
	  # Get channels of both images.
	  prevBlue, prevGreen, prevRed = prevImage[y,x]
	  blue, green, red = image[y,x]

	  # Take luminosity into account by assuming that a change of 10 is permited. If more, then motion was detected.
	  if math.fabs(prevBlue - blue) > 10 and math.fabs(prevGreen - green) > 10 and math.fabs(prevRed - red) > 10:
		# Update pixel count and, if greater than threshold, say that motion was detected.
		differentPixels = differentPixels + 1
		
		if differentPixels >= 10:
		 print "Motion detected!!"
		 break
	
	# Show the image
	cv.ShowImage("Motion", image)	
	waitKey(1)

	# Update previous image
	cv.SaveImage('motion1.jpg',image)
