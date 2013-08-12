#!/usr/bin/env python
'''
This program searches a blob of a given color in the video and calculates 
its center, marking it with a red cross. The windows shows the blob marked in black
and its center.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
import cv
from cv2 import *

# Open the webcam
cam= VideoCapture(0)

# View for the final image
# *** USER: change the name of the window that will show the video.
namedWindow("Webcam feed", cv.CV_WINDOW_AUTOSIZE)

while True:
	# x and y position accumulators
	acc_x = 0
	acc_y = 0

	# number of pixels accumulated
	acc_count = 0

	# grab an image from the camera
	s, image = cam.read()
	if s:
		# *** USER: change name of file
		imwrite('cam_image.jpg', image)
		
	image = cv.LoadImage('cam_image.jpg')	

	for x in range(0, image.height):
  	  for y in range(0, image.width):
    	# get the value of the current pixel
    	blue, green, red = image[x, y]

   		# check if the blue intensity is greater than the green
   		# *** USER: change the color of the blob that is going to be detected.
   		if blue > green and blue > red and blue > 128:
		 # add x and y to accumulators
		 acc_x += x
		 acc_y += y
		 # increment accumulated pixels count
		 acc_count += 1
		 image[x, y] = 0, 0, 0

	# check the count accumulator is greater than zero, to avoid dividing by zero
	if acc_count > 0:
 	 # calculate the mean x and y positions
 	 mean_x = acc_x / acc_count
 	 mean_y = acc_y / acc_count

 	 # draw a small cross in red at the mean position
 	 # *** USER: change the color of the cross.
 	 image[mean_x + 0, mean_y - 1] = 0, 0, 255
 	 image[mean_x - 1, mean_y + 0] = 0, 0, 255
  	 image[mean_x + 0, mean_y + 0] = 0, 0, 255
  	 image[mean_x + 1, mean_y + 0] = 0, 0, 255
  	 image[mean_x + 0, mean_y + 1] = 0, 0, 255

	# display the image on the screen
	cv.ShowImage("Webcam feed", image)
	waitKey(1)
