#!/usr/bin/env python
'''
This program let's you check that your webcam and OpenCV work correctly
with your Raspberry Pi. The video will be showed in a window.

The *** USER tag in the comments is to point good places where the user 
can modify it for his own purpouses.
'''
from cv2 import *

# Open the webcam
cam= VideoCapture(0)

# View for the final image
# *** USER: change the name of the output window.
namedWindow("Webcam feed", cv.CV_WINDOW_AUTOSIZE)

while True:
	# grab an image from the camera
    s, image = cam.read()
    if s:
		# *** USER: change name of file
		imwrite('cam_image.jpg', image)

    my_image = imread('cam_image.jpg')
    
    # display the image on the screen
    imshow("Webcam feed", my_image)
    waitKey(1)
