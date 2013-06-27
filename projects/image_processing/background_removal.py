#!/usr/bin/env python
from imgproc import *
import time

# Open the webcam
cam= Camera(20, 15)

# View for the final image
view = Viewer(cam.width, cam.height, "Background removed")

while True:

	# grab an image from the camera
	my_image = cam.grabImage()	

	# iterate over ever pixel in the image by iterating 
	# over each row and column
	for x in range(0, my_image.width):
  	  for y in range(0, my_image.height):
    		# get the value of the current pixel
    		red, green, blue = my_image[x, y]

   		# check if the intensities are near to white colour
   		if green > 200 and red > 200 and blue > 200:      		 
      			# this pixel is predominantly white
      			# let's set it to black
      			my_image[x, y] = 0, 0, 0	

	# display the image on the screen
	view.displayImage(my_image)
