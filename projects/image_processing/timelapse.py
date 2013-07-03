#!/usr/bin/python
from cv2 import *
import datetime
import time

# Set camera
cam = VideoCapture(2)

# Read from the camera and save the image in the given place.
while True:
 # Get current date and time
 now = datetime.datetime.now()

 s, image = cam.read()
 if s:
  imwrite("image"+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+".jpg", image)

 time.sleep(4)
