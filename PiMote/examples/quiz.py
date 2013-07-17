"""
An example application using pimote
To run: python regular.py
  this will run it on ip=0.0.0.0 port=8090

Needs porting into python3 for use with the PiFace interface

"""

import sys, threading, time
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from pimote import *


# Parse the IP address and port you wish to listen on.
try:
	ip = sys.argv[1]
	port = int(sys.argv[2])
except:
	ip = "0.0.0.0"
	port = 8090

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	#Override
	def buttonPressed(self, id, message, phoneId):
		#########----------------------------------------------###########
		# Your code will go here! Check for the ID of the button pressed #
		# and handle that button press as you wish.                      #
		#########----------------------------------------------###########
		if id == a.getId() and Globals.correct == "A":
			print("Correct!")
			Globals.answer = True
		elif id == b.getId() and Globals.correct == "B":
			print("Correct!")
			Globals.answer = True
		elif id == c.getId() and Globals.correct == "C":
			print("Correct!")
			Globals.answer = True
		else:
			print("Wrong")

outputQA = OutputText("QA")
a = Button("A")
b = Button("B")
c = Button("C")
s = Spacer(100)
s2 = Spacer(50)

# Create the phone object
thisphone = MyPhone()
thisphone.setTitle("PiQuiz")

thisphone.addSpace(s2)
thisphone.addOutput(outputQA)
thisphone.addSpace(s)
thisphone.addButton(a)
thisphone.addButton(b)
thisphone.addButton(c)
#Create the server
myserver = PhoneServer()
myserver.setPassword("helloworld")
myserver.setMaxClients(2)

#Add the phone
myserver.addPhone(thisphone)

class Questioner(threading.Thread):
	def run(self):
		lines = []
		f = open("qa.txt", "r")
		for line in f:
			lines.append(line.strip("\n"))
		lineCount = 0

		while Globals.running and lineCount < len(lines):
			try:
				Globals.answer = False
				q = lines[lineCount]
				a = lines[lineCount+1]
				b = lines[lineCount+2]
				c = lines[lineCount+3]
				k = lines[lineCount+4]
				lineCount += 5
				#display
				que = str(str(q)+"&/&/"+str(a)+"&/"+str(b)+"&/"+str(c))
				outputQA.setText(que)
				Globals.correct = k
				#Wait for answer
				while not Globals.answer:
					time.sleep(0.5)
			except Exception, e:
				print("Error:" + str(e))
				Globals.running = False

		print("DONE")

class Globals:
	running = True
	answer = False
	correct = ""

l = Questioner()
l.start()
# Start server
myserver.start(ip, port)