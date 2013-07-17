#!/usr/bin/env python

from imgproc import *
from time import sleep

# open the webcam
#camera = Camera(640, 480)
camera = Camera(320, 240)
#camera = Camera(160, 120)

#while True:
	
	# grab an image from the camera
frame = camera.grabImage()

print frame[x,y]

	# open a view, setting the view to the size of the captured image
	#view = Viewer(frame.width, frame.height, "Basic image processing")

	# display the image on the screen
	#view.displayImage(frame)




"""
	width, height = 320, 240
	#HUD = Image.new()
	HUD = Image.open("HUDs/preview_320x240.png")
	
	
	for x in range(width):
		for y in range(height):
			red1, green1, blue1 = frame[x,y]
			red2, green2, blue2, alpha = HUD.getpixel((x,y))
			
			if red2 != 0 and green2 != 0 and blue2 != 0:
				frame[x,y] = red2, green2, blue2
"""