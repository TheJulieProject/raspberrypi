#!/usr/bin/env python
from imgproc import *
import time

# function to obtain the command in words.
def calc_command(number):
 if number < 5:
  if number == 1:
	return "Right_Forward"
  elif number == 2:
	return "Forward"
  elif number == 3:
	return "Left_Forward"
  else:
	return "Turn_Right"
 elif number > 5:
  if number == 7:
	return "Right_Back"
  elif number == 8:
	return "Back"
  elif number == 9:
	return "Left_Back"
  else:
	return "Turn_Left"
 else:
  return "Nothing"

# Open the webcam
cam= Camera(20, 15)

while True:

	# x and y position accumulators
	acc_x = 0
	acc_y = 0

	# Number of pixels accumulated
	acc_count = 0

	# Current coordinate. Initially is 5 as it represent the centre
	# of the grid, which means do nothing.
	coordinate = 5

	# Take an image from the camera
	image = cam.grabImage()

	for x in range(0, image.width):
  	  for y in range(0, image.height):
    		# Get the value of the current pixel
    		red, green, blue = image[x, y]

   		# check if the blue intensity is greater than the green
   		if blue > green and blue > red and blue > 180 and green > 60:
		 # add x and y to accumulators
		 acc_x += x
		 acc_y += y
		 # increment accumulated pixels count
		 acc_count += 1		

	# check the count accumulator is greater than zero, to avoid dividing by zero
	if acc_count > 0:
 	 # Calculate the mean x and y positions
 	 mean_x = acc_x / acc_count
 	 mean_y = acc_y / acc_count

 	 # Calculate where is the centre of the object in our grid.
	 # Check if the point is in the first column.
	 if mean_x < image.width / 3:
	  if mean_y < image.height / 3:
		coordinate = 1
	  elif mean_y < image.height * 2 / 3:
		coordinate = 4
	  else:
		coordinate = 7
	 # Check the second column
	 elif mean_x < image.width * 2 / 3:
	  if mean_y < image.height / 3:
		coordinate = 2
	  elif mean_y < image.height * 2 / 3:
		coordinate = 5
	  else:
		coordinate = 8
	 # Finally the third column
	 else:
	  if mean_y < image.height / 3:
		coordinate = 3
	  elif mean_y < image.height * 2 / 3:
		coordinate = 6
	  else:
		coordinate = 9

	# Calculate the command corresponding to the coordinate and print it
	print calc_command(coordinate)

	# Wait a second
	time.sleep(1.5)
