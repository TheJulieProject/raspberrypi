#!/usr/bin/env python
from cv2 import *
import os
import time

# View for the final image
namedWindow("Webcam feed", cv.CV_WINDOW_AUTOSIZE)

while True:	
    # grab an image from the camera
    os.system("raspistill -w 400 -h 300 -t -1 -n -o cam_image.jpg -e jpg")  
    
    image = imread("cam_image.jpg")
    imshow("Webcam feed", image)
    waitKey(1)
    
