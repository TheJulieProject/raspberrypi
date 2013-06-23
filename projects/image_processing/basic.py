#!/usr/bin/env python
from imgproc import *
import time

# open the webcam
my_camera = Camera(160, 120)

while True:

	# grab an image from the camera
	my_image = my_camera.grabImage()

	# open a view, setting the view to the size of the captured 
	# image
	my_view = Viewer(my_image.width, my_image.height, 
			 "Basic image processing")

	"""# iterate over ever pixel in the image by iterating 
	# over each row and each column
	for x in range(0, my_image.width):
  	  for y in range(0, my_image.height):
    		# get the value of the current pixel
    		red, green, blue = my_image[x, y]

   		# check if the blue intensity is greater than the green
   		if blue > green:
      		 # check if blue is also more intense than red
      		 if blue > red:
      			# this pixel is predominantly blue
      			# let's set it to red
      			my_image[x, y] = 255, 0, 0"""	

	# display the image on the screen
	my_view.displayImage(my_image)
	

	