#!/usr/bin/env python
'''
This programs takes an image and changes the background for a given one. 
It shows in two windows the original with the background detected and colore
d as black and the image with the background changed.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
from cv2 import *
import cv

# Open the webcam
cam= VideoCapture(0)

# Create two views, one for the original image and another for the image with the background deleted
# *** USER: change the names of the windows.
namedWindow("Without background", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Another background", cv.CV_WINDOW_AUTOSIZE)

while True:
	# grab an image from the camera
	s, image = cam.read()
	if s:
		# *** USER: change name of file
		imwrite('cam_image.jpg', image)

	my_image = cv.LoadImage('cam_image.jpg')	

	# Get destiny image
	# *** USER: change destiny image.
	destiny = cv.LoadImage("green_wall-wallpaper-320x240.jpg")

	# iterate over ever pixel in the image by iterating 
	# over each row and each column
	for x in range(0, my_image.height):
  	  for y in range(0, my_image.width):
		  # get the value of the current pixel
		  blue, green, red = my_image[x, y]
		  
		  # check if the intensity is near white
		  # *** USER: change color that will be detected and deleted.
		  if green > 180 and red > 180 and blue > 120:
			  # this pixel is predominantly white let's set it to black
			  # *** USER: change the color that will appear in the removed places.
			  my_image[x, y] = 0, 0, 0
		  # If it shouldn't be deleted, then copy to the destiny image
		  else:
			  destiny[x,y] = blue,green,red

	# *** USER: Save destiny image if you desire so
	cv.SaveImage("Image_background_changed.jpg",destiny)

	# display the images on the screen
	cv.ShowImage("Without background", my_image)
	cv.ShowImage("Another background", destiny)
	cv.WaitKey(1)
