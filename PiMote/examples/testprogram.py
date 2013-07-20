"""
An example application using pimote
To run: python testprogram.py
  this will run it on ip=0.0.0.0 port=8090

Needs porting into python3 for use with the PiFace interface

"""

import sys, random
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
		if id == b1.getId():
			if b2.getValue() == True:
				b2.setValue(False)
			else:
				b2.setValue(True)

			self.updateDisplay()
		elif id == b2.getId():
			o1.setText("Toggle switched to " + message)
		elif id == b3.getId():
			o1.setText(message)
		elif id == r.getId():
			i = random.randint(0, 100)
			p.setProgress(i)
			o2.setText(str(i)+"%")

		o3.setText("Input from ID: " + str(phoneId))

# Create the phone object
thisphone = MyPhone()
thisphone.setTitle("Example PiMote App")
p = ProgressBar(120)
b1 = Button("Hello") #Regular button
b2 = ToggleButton("This is a toggle button", True) #Toggle
b3 = InputText("Input text here") #Text Input
o1 = OutputText("Output")
o2 = OutputText("0") #Output field
v = VideoFeed(640, 480) #Live video feed
v2 = VideoFeed(640, 480) #Live video feed
vi = VoiceInput() #Voice input
s = Spacer(100)
r = RecurringInfo(2000)
o3 = OutputText("Input from ID: ?")

#Add the buttons to the phone
thisphone.addButton(b1)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addOutput(o1)
thisphone.addSpace(s)
thisphone.addOutput(p)
thisphone.addOutput(o2)
thisphone.addButton(r)
thisphone.addButton(vi)

#Create the server
myserver = PhoneServer()
myserver.setPassword("helloworld")
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)