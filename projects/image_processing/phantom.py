import cv2
import numpy as np

# Set webcam
cam = cv2.VideoCapture(0)

# Read image
_,f = cam.read()

avg1 = np.float32(f)
avg2 = np.float32(f)

while True:
	# Get image
	_,f = c.read()

	cv2.accumulateWeighted(f,avg1,0.1)
	cv2.accumulateWeighted(f,avg2,0.01)

	res1 = cv2.convertScaleAbs(avg1)
	res2 = cv2.convertScaleAbs(avg2)
	
	# Show images
	cv2.imshow('img',f)
	cv2.imshow('avg1',res1)
	cv2.imshow('avg2',res2)
	k = cv2.waitKey(20)

	# close windows
	if k == 27:
	 break

cv2.destroyAllWindows()
cam.release()