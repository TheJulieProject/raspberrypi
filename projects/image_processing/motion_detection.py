#!/usr/bin/env python
'''
This program detects motion in a video by comparing the pixels of the previous
frame and the current one, printing the information on the terminal. A window
shows the video feed.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
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
	# *** USER: change the name of the file.
	imwrite('motion1.jpg', image)

while True:
	# Initialise pixel count
	differentPixels = 0

	# Open previous image 
	prevImage = cv.LoadImage('motion1.jpg')

	# Take another image
	s, image = cam.read()
	if s:
		# *** USER: change filename
		imwrite('motion2.jpg', image)

	# Read it
	image = cv.LoadImage('motion2.jpg')

	# Iterate through each pixel comparing the ones of both images.
	for y in range(0, image.height):
         for x in range(0, image.width):
			 # Get channels of both images.
			 prevBlue, prevGreen, prevRed = prevImage[y,x]
			 blue, green, red = image[y,x]
			 
			 # Take luminosity into account by assuming that a change of 20 is permited. 
			 # If more, then motion was detected.
			 # *** USER: change the threshold.
			 if math.fabs(prevBlue - blue) > 20 or math.fabs(prevGreen - green) > 20 or math.fabs(prevRed - red) > 20:
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
