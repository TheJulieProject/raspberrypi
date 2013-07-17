#!/usr/bin/env python
from cv2 import *
import os
import time

while True:
	# grab an image from the camera
    os.system("raspistill -w 400 -h 300 -t 0 -n -o cam_image.jpg")    
   
