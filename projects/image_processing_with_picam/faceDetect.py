#!/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

TODO: make into a class
TODO: use optparser


Original C implementation by:  ?
Python implementation by: Roman Stanchak
Modified for pygame by: Brian Thorne
Modified for Raspberry Pi by: Diego Abel
"""
import sys
import cv as opencv
from cv import *

# Global Variables and Settings
cascade = None
storage = CreateMemStorage(0)

#cascade_name = "haarcascade_frontalface_alt.xml"
# CHOOSE HERE
cascade_name = "haarcascade_eye.xml"
#cascade_name =  "haarcascade_frontalface_default.xml"

# This is what we do the processing on - if a int (inside a string) it will load /dev/video<int>
input_name = '0'    

# Settings end here
###############################################################################

NamedWindow( "result", 1 )

# the OpenCV API says this function is obsolete, but we can't
# cast the output of cvLoad to a HaarClassifierCascade, so use this anyways
# the size parameter is ignored
cascade = Load(cascade_name)

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size
mat = CreateMat(20,20, CV_32FC1)
min_size = GetSize(mat)
image_scale = 1.3
haar_scale = 1.1
min_neighbors = 3
haar_flags = 0


def detectObject(img):
    gray = CreateImage( GetSize(img), 8, 1 )
    small_img = CreateImage(GetSize(img),8, 1 )
    CvtColor(img, gray, CV_BGR2GRAY)
    Resize( gray, small_img, CV_INTER_LINEAR )

    EqualizeHist( small_img, small_img )
    
    #ClearMemStorage( storage )

    if( cascade ):
        t = GetTickCount()
        faces = HaarDetectObjects( small_img, cascade, storage,
                                     haar_scale, min_neighbors, haar_flags, min_size )
        t = GetTickCount() - t
        print "%i objects found, detection time = %gms" % (len(faces),t/(GetTickFrequency()*1000.))
        return faces
    else:
        print "no cascade"
    
def detect_and_draw( img ):
    """
    draw a box with opencv on the image around the detected faces.
    """
    faces = detectObject(img)
    if faces:
        for (x,y,w,h),n in faces:
	    print "Face found at (x,y) = (%i,%i)" % (x,y)	                
            Rectangle( img, (x,y), (x+w,y+h), CV_RGB(255,0,0))
    ShowImage( "result", img ) # TODO is this reqd if pygame renders?
    return img

def main():
    if len(sys.argv) > 1:

        if sys.argv[1].startswith("--cascade="):
            cascade_name = sys.argv[1][ len("--cascade="): ]
            if len(sys.argv) > 2:
                input_name = sys.argv[2]

        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print "Usage: facedetect --cascade=\"<cascade_path>\" [filename|camera_index]\n" 
            sys.exit(-1)

        else:
            input_name = sys.argv[1]
    
    # Global Variables
    from faceDetect import cascade, input_name

    if not cascade:
        print "ERROR: Could not load classifier cascade"
        sys.exit(-1)
    

    if input_name.isdigit():
        capture = CreateCameraCapture( int(input_name) )
    else:
        capture = CreateFileCapture( input_name )

    NamedWindow( "result", 1 )

    if( capture ):
        frame_copy = None
        while True: 
            frame = QueryFrame( capture )
            if( not frame ):
                break;
            if( not frame_copy ):
                frame_copy = CreateImage( GetSize(frame),
                                            IPL_DEPTH_8U, frame.nChannels )
            if( frame.origin == IPL_ORIGIN_TL ):
                Copy( frame, frame_copy )
            else:
                Flip( frame, frame_copy, 0 )
            
            detect_and_draw( frame_copy )

            if( WaitKey( 10 ) >= 0 ):
                break;

    else:
        image = LoadImage( input_name, 1 )

        if( image ):
        
            detect_and_draw( image )
            WaitKey(0)
        
    DestroyWindow("result")

if __name__ == '__main__':
    main()
