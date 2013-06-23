#!/usr/bin/env python
from imgproc import *
import time

# open the webcam
cam= Camera(20, 15)

# open a view, setting the view to the size of the captured image
view = Viewer(cam.width, cam.height, "Blob finding")

while True:

	# grab an image from the camera
	my_image = cam.grabImage()	

	# iterate over ever pixel in the image by iterating 
	# over each row and each column
	for x in range(0, my_image.width):
  	  for y in range(0, my_image.height):
    		# get the value of the current pixel
    		red, green, blue = my_image[x, y]

   		# check if the blue intensity is greater than the green
   		if green > 200 and red > 200 and blue > 200:      		 
      			# this pixel is predominantly blue
      			# let's set it to black
      			my_image[x, y] = 0, 0, 0	

	# display the image on the screen
	view.displayImage(my_image)