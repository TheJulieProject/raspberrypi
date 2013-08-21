# Setting the Raspberry Pi Camera
This instructions will let you use the code in this folder with your 
Raspberry Pi and its camera.

## Requirements

A Raspberry Pi

A Pi camera 

## Connecting the camera to the RPi

The first thing you need to do is to follow the instructions in the 
Raspberry Pi webpage (www.raspberrypi.org/camera) in order to get the
camera working.

## Getting the official Pi camera API

Once the camera is working, it is time to download its API from the 
github page: https://github.com/raspberrypi/userland (use the command git clone).

## Installing software

The next thing you need to do is to install CMake and OpenCV. In order to do that,
just run the following commands:

	sudo apt-get update
	sudo apt-get install cmake libopencv-dev python-opencv

## Running a program

In order to run a program you just have to compile the provided CMakeList 
(ensuring first that the paths and file names are correct). In order to do that, 
just enter in the folder where the files are and type in the terminal:

	cmake .
	make
	./filename
	
Where filename is the name of the file you want to be executed.

NOTE that if youy modify the CMakeList in order to get another program working, 
you don't need to execute the cmake command again; with the make will be enough.	
