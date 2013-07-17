#!/usr/bin/env python
from cv2 import *
import os
import time

# View for the final image
namedWindow("Webcam feed", cv.CV_WINDOW_AUTOSIZE)

while True:	
    image = imread("cam_image.jpg")
    imshow("Webcam feed", image)
    waitKey(1)
    
