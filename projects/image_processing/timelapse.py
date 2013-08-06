#!/usr/bin/python
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
  imwrite("image"+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+".jpg", image)

 # Wait 4 seconds
 time.sleep(4)
