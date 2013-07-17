#!/usr/bin/env python
import cv
from cv2 import *

# Open the webcam
cam= VideoCapture(0)

# View for the final image
namedWindow("Without background", cv.CV_WINDOW_AUTOSIZE)

while True:

	# grab an image from the camera
	s, image = cam.read()
	if s:
	 imwrite('cam_image.jpg', image)

	my_image = cv.LoadImage('cam_image.jpg')

	# iterate over ever pixel in the image by iterating 
	# over each row and column
	for x in range(0, my_image.height):
  	  for y in range(0, my_image.width):
    		# get the value of the current pixel
    		blue, green, red = my_image[x, y]

   		# check if the intensities are near to white colour
   		if green > 180 and red > 180 and blue > 120:      		 
      			# this pixel is predominantly white
      			# let's set it to black
      			my_image[x, y] = 0, 0, 0	

	# Save image if you want
	cv.SaveImage("image_without_background.jpg", my_image)

	# display the image on the screen
	cv.ShowImage("Without background", my_image)
	waitKey(1)
