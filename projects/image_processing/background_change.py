#!/usr/bin/env python
from imgproc import *
import cv

# Open the webcam
cam= Camera(20, 15)

# Create two views, one for the original image and another for the image with the background deleted
view = Viewer(cam.width, cam.height, "Normal feed")
cv.NamedWindow("Another background", cv.CV_WINDOW_AUTOSIZE)

while True:

	# grab an image from the camera
	my_image = cam.grabImage()	

	# Get destiny image
	destiny = cv.LoadImage("green_wall-wallpaper-320x240.jpg")

	# iterate over ever pixel in the image by iterating 
	# over each row and each column
	for x in range(0, my_image.width):
  	  for y in range(0, my_image.height):
    		# get the value of the current pixel
    		red, green, blue = my_image[x, y]

   		# check if the intensity is near white
   		if green > 200 and red > 200 and blue > 200:      		 
      			# this pixel is predominantly white
      			# let's set it to black
      			my_image[x, y] = 0, 0, 0
		# If it shouldn't be deleted, then copy to the destiny image
    		else:
		 destiny[y,x] = blue,green,red

	# display the images on the screen
	view.displayImage(my_image)
	cv.ShowImage("Another background", destiny)
	cv.WaitKey(1)
