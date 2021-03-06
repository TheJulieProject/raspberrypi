#!/usr/bin/env python
import cv
from cv2 import *

# Set windows to show results
namedWindow("Normal feed", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Edge detection", cv.CV_WINDOW_AUTOSIZE)

# Set camera
cam = VideoCapture(0)

while True:
 # Read from the camera
 s, image = cam.read()
 if s:
	# *** USER: change name of file
	imwrite('cam_image.jpg', image)

 # Code from stack overflow (# TODO: find the link)
 # Open the image
 image = cv.LoadImage('cam_image.jpg') 

 yuv = cv.CreateImage(cv.GetSize(image),8,3)
	
 # convert to grey
 gray = cv.CreateImage(cv.GetSize(image),8,1)
 cv.CvtColor(image,yuv, cv.CV_BGR2YCrCb)
 cv.Split(yuv,gray, None,None,None)

 # Use canny algorithm for edge detection
 canny = cv.CreateImage(cv.GetSize(image),8,1)
 cv.Canny(gray,canny,50,200)
 
 # *** USER: Save the image
 cv.SaveImage("Canny.jpg", canny)

 # Show the images
 cv.ShowImage("Normal feed", image)
 cv.ShowImage("Edge detection", canny)	
 waitKey(1)	
	
