"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace

"""

import sys, random
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from pimote import *


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	#Override
	num = 0
	def buttonPressed(self, id, message):
		#########----------------------------------------------###########
		# Your code will go here! Check for the ID of the button pressed #
		# and handle that button press as you wish.                      #
		#########----------------------------------------------###########
		if id == b1.getId():
			o1.setText("Hello world")
		elif id == b2.getId():
			o1.setText("Toggle switched to " + message)
		elif id == b3.getId():
			o1.setText(message)
		elif id == r.getId():
			num = random.randint(0,120)
			p.setProgress(num)
			o2.setText(str(num))

# Create the phone object
thisphone = MyPhone()
thisphone.setTitle("Example PiMote App")
p = ProgressBar(120)
b1 = Button("Hello") #Regular button
b2 = ToggleButton("This is a toggle button", True) #Toggle
b3 = InputText("Input text here") #Text Input
o1 = OutputText("Output")
o2 = OutputText("0") #Output field
v = VideoFeed(320, 240) #Live video feed
vi = VoiceInput() #Voice input
s = Spacer(100)
r = RecurringInfo(2000)

#Add the buttons to the phone
thisphone.addButton(b1)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addOutput(o1)
thisphone.addSpace(s)
thisphone.addOutput(p)
thisphone.addOutput(o2)
thisphone.addSpace(s)
thisphone.addVideoFeed(v)
thisphone.addButton(r)
#Create the server
myserver = PhoneServer()
myserver.setPassword("helloworld")
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)

