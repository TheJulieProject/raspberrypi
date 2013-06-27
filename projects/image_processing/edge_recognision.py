#!/usr/bin/env python
import cv
from cv2 import *
import numpy as np

namedWindow("Normal feed", cv.CV_WINDOW_AUTOSIZE)
namedWindow("Edge detection", cv.CV_WINDOW_AUTOSIZE)
cam = VideoCapture(0)

while True:
 s, image = cam.read()
 if s:
  imwrite('cam_image.jpg', image)

 # Code from stack overflow
 # Open the image
 image = cv.LoadImage('cam_image.jpg') 

 yuv = cv.CreateImage(cv.GetSize(image),8,3)
	
 # convert to grey
 gray = cv.CreateImage(cv.GetSize(image),8,1)
 cv.CvtColor(image,yuv, cv.CV_BGR2YCrCb)
 cv.Split(yuv,gray, None,None,None)

 canny = cv.CreateImage(cv.GetSize(image),8,1)
 cv.Canny(gray,canny,50,200)

 #Show the images
 cv.ShowImage("Normal feed", image)
 cv.ShowImage("Edge detection", canny)	
 waitKey(1)	
	