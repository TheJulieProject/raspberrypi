#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *

from time import sleep


#-----------------------------------------------------
class NXTRobot:

	def __init__(self):

		nxtBrick = nxt.locator.find_one_brick()

		self.leftMotor  = Motor(nxtBrick, PORT_A)
		self.rightMotor = Motor(nxtBrick, PORT_C)
		
		#self.lightSensor = Light(nxtBrick, PORT_3)
		self.ultrasonicSensor = Ultrasonic(nxtBrick, PORT_4)


	def leftMotor(self, enabled, direction):
		
		if enabled == True:
			if direction == 1:
				self.leftMotor.run(power = 100)
			else:
				self.leftMotor.run(power = -100)

		else:
			self.leftMotor.idle()

	
	def rightMotor(self, enabled, direction):
		
		if enabled == True:
			if direction == 1:
				self.rightMotor.run(power = 100)
			else:
				self.rightMotor.run(power = -100)

		else:
			self.rightMotor.idle()


	#def getLightReading(self)
	#	return self.lightSensor.get_sample


	def getUltrasonicReading(self):
		return self.ultrasonicSensor.get_sample()

