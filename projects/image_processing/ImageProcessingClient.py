"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace
"""

# Import
import sys
from pimoteutils import *
# import 
import move_robot_with_hands as moveRobot

# Parse the IP address and port you wish to listen on.
ip = sys.argv[1] 		
port = int(sys.argv[2]) 

# Messages to PiDroid are sent as
# ("ROBOT_CONTROL,ACTION")
ROBOT_CONTROL = "0"

# ROBOT_CONTROL actions
BOTH_OFF 	= "1,0,-1"

LEFT_OFF 	= "1,0,0" 
LEFT_UP 	= "1,0,1"
LEFT_DOWN	= "1,0,3"

RIGHT_OFF 	= "1,0,4"
RIGHT_UP	= "1,0,5"
RIGHT_DOWN	= "1,0,7"

#
PROCESS_IMAGES_OFF = "0"
PROCESS_IMAGES_ON  = "1"



class ImageProcessingClient(Client):
	
	def onStart(self):
		print "Client started."

	def onMessage(self, message):
		if   message == PROCESS_IMAGES_ON:
			self.processing = True
		elif message == PROCESS_IMAGES_OFF:
			self.processing = False
		else:
			print "SERVER ERROR: Message not recognised."



myClient = ImageProcessingClient()
myClient.start(ip, port)


while myClient.isRunning():
	try: 
		if myClient.processing == True:
			command = moveRobot.move()
			commandRight, commandLeft = command.split("_")
			if commandLeft == "1":
				myClient.send(LEFT_UP)
			elif commandLeft == "-1":
				myClient.send(LEFT_DOWN)
			elif commandLeft == "0":
				myClient.send(LEFT_OFF)
			elif commandLeft == "Do nothing":
				pass
			else:
				print "ERROR: Invalid image processing output to server"

			if commandRight == "1":
				myClient.send(RIGHT_UP)
			elif commandRight == "-1":
				myClient.send(RIGHT_DOWN)
			elif commandRight == "0":
				myClient.send(RIGHT_OFF)
			elif commandRight == "Do nothing":
				pass
			else:
				print "ERROR: Invalid image processing output to server"
	except:
		myClient.stop()


myClient.stop()
