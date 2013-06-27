"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace
"""

# Import PhoneServer and Phone classes from pimoteutils.
import sys
from pimoteutils import *


#
import subprocess
import cleverbot


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])


# message IDs and used literals
ROBOT_CONTROL = "0"
VOICE_CONTROL = "1"

LEFT_FORWARDS_OFF  = "0"
LEFT_FORWARDS_ON   = "1"
LEFT_BACKWARDS_OFF = "2"
LEFT_BACKWARDS_ON  = "3"

RIGHT_FORWARDS_OFF  = "4"
RIGHT_FORWARDS_ON   = "5"
RIGHT_BACKWARDS_OFF = "6"
RIGHT_BACKWARDS_ON  = "7"

BOTH_OFF = "-1"

ROBOT_ENABLED = 0	# 0 = OFF, 1 == ON; for testing purposes


# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class PiDroid(ControllerPhone):
	
	def __init__(self):
		self.speak = False
		self.conversation = False
		self.PiAI = cleverbot.Session()


	def controlPress(self, msg):
		(id, sep, message) = msg.strip().partition(",")

		print "received: " + msg

		if   id == ROBOT_CONTROL:
			self.moveRobot(message, power = 100)
		
		elif id == VOICE_CONTROL:
			self.interpretVoice(message)


	def say(self, something):
		size = 99
		if len(something) > size:
			words = something.split()

			toBeSpoken = ""
			for word in words:
				if len(toBeSpoken) + len(word) < size:
					toBeSpoken = toBeSpoken + " " + word
				else:
					print toBeSpoken
					cmd = ['./speech.sh', toBeSpoken]
					p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
					p.wait()
					toBeSpoken = word
			cmd = ['./speech.sh', toBeSpoken]
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE)			
		else:
			cmd = ['./speech.sh', something]
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		p.wait()


	def reply(self, toSomething):
		answer = self.PiAI.Ask(toSomething)
		print "replied: " + answer
		self.say(answer)


	def moveRobot(self, message, power):
		
		if ROBOT_ENABLED == 0:
			return

		if   message == LEFT_FORWARDS_OFF:
			nxt.leftMotor.idle()
		
		elif message == LEFT_FORWARDS_ON:
			nxt.leftMotor.run(power)
		
		elif message == LEFT_BACKWARDS_OFF:
			nxt.leftMotor.idle()
		
		elif message == LEFT_BACKWARDS_ON:
			nxt.leftMotor.run(-power)
		

		elif message == RIGHT_FORWARDS_OFF:
			nxt.rightMotor.idle()
		
		elif message == RIGHT_FORWARDS_ON:
			nxt.rightMotor.run(power)
		
		elif message == RIGHT_BACKWARDS_OFF:
			nxt.rightMotor.idle()

		elif message == RIGHT_BACKWARDS_ON:
			nxt.rightMotor.run(-power)

		elif message == BOTH_OFF:
			nxt.leftMotor.idle()
			nxt.rightMotor.idle()

		else:
			print 'ERROR: received ' + message + ' as ROBOT_CONTROL'


	def interpretVoice(self, message):

		if self.speak == True and self.conversation == False:
			if message.isdigit() == False:
				self.say(message)	

		elif self.speak == True and self.conversation == True:
			if message.isdigit() == False:
				self.reply(message)			

		power = 80

		if message == "forwards" or message == "go forwards":
			self.moveRobot(LEFT_FORWARDS_ON, power)		#
			self.moveRobot(RIGHT_FORWARDS_ON, power)	#

		elif message == "backwards" or message == "go backwards":
			self.moveRobot(LEFT_BACKWARDS_ON, power)	#
			self.moveRobot(RIGHT_BACKWARDS_ON, power)	#
			
		elif message == "turn left" or message == "spin left":
			self.moveRobot(LEFT_BACKWARDS_ON, power)	#
			self.moveRobot(RIGHT_FORWARDS_ON, power)	#

		elif message == "turn right" or message == "spin right":
			self.moveRobot(LEFT_FORWARDS_ON, power)		#
			self.moveRobot(RIGHT_BACKWARDS_ON, power)	#

		elif message == "stop":
			self.moveRobot(BOTH_OFF)	#


		elif message == "speak to me":
			self.speak = True
			self.say("I can talk! Horay!")

		elif message == "stop speaking":
			self.self = False
			self.conversation = False
			self.say("You are being mean to PiDroid, human")

		elif message == "let's talk":
			self.speak = True
			self.conversation = True
			self.say("Very well, human. Let's have a chat.")

		elif message == "goodbye":
			self.conversation = False
			self.say("This has been midly entertaining. Until next time, human.")
		

# Create the phone object
PiDroid = PiDroid()
PiDroid.setVideo(True)
PiDroid.setVoice(True)

# Enabling the NXT Lego Robot
if ROBOT_ENABLED == 1:
	import robot_interf as r
	nxt = r.NXTRobot()

#Create the server
myserver = PhoneServer()
myserver.setPassword("helloworld")
#Add the phone (app)
myserver.addPhone(PiDroid)
# Start server
myserver.start(ip, port)
