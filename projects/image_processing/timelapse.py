#!/usr/bin/env python
'''
This program runs until it is stopped, taking an image each 4 seconds,
resulting in a timelapse.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
from cv2 import *
import datetime
import time

# Set camera
cam = VideoCapture(2)

while True:
 # Get current date and time
 now = datetime.datetime.now()

 # Read from the camera and save the image in the given place.
 s, image = cam.read()
 if s:
	 # *** USER: change the name of the file.
	 imwrite("image"+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+".jpg", image)

 # Wait 4 seconds
 # *** USER: modify the waiting time between pictures.
 time.sleep(4)
