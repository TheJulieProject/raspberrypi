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
	
	# display the image on the screen
	my_view.displayImage(my_image)
	

	