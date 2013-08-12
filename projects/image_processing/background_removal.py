#!/usr/bin/env python
'''
This programs takes an image and sets to black all the background detected as
white. It shows in two windows the original and modified image.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
import cv
from cv2 import *

# Open the webcam
cam= VideoCapture(0)

# View for the final image
# *** USER: change the name of the window.
namedWindow("Without background", cv.CV_WINDOW_AUTOSIZE)

while True:

	# grab an image from the camera
	s, image = cam.read()
	if s:
		# *** USER: change name of file
		imwrite('cam_image.jpg', image)

	my_image = cv.LoadImage('cam_image.jpg')

	# iterate over ever pixel in the image by iterating 
	# over each row and column
	for x in range(0, my_image.height):
  	  for y in range(0, my_image.width):
		  # get the value of the current pixel
		  blue, green, red = my_image[x, y]
		  
		  # check if the intensities are near to white color
		  # *** USER: change color that will be detected and deleted.
		  if green > 180 and red > 180 and blue > 120: 
			# this pixel is predominantly white let's set it to black
			# *** USER: change the color that will appear in the removed places.
			my_image[x, y] = 0, 0, 0	

	# *** USER: Save image if you want
	cv.SaveImage("image_without_background.jpg", my_image)

	# display the image on the screen
	cv.ShowImage("Without background", my_image)
	waitKey(1)
