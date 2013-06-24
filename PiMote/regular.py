"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace

"""

import sys
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from pimoteutils import *


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	#Override
	text = "Hello"
	def buttonPressed(self, id, message):
		if id == b1.getId():
			o1.setText(self.text)
			if self.text == "Hello":
				self.text = "World"
			else:
				self.text = "Hello"
		elif id == b2.getId():
			print("Toggle switched to " + str(message))
		elif id == b3.getId():
			o1.setText(message)

# Create the phone object
thisphone = MyPhone()

b1 = Button("Hello")
b2 = ToggleButton("This is a toggle button", True)
b3 = InputText("Input text here")
o1 = OutputText("Hello")

thisphone.addButton(b1)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addOutput(o1)
#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)
