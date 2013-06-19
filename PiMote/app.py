"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace

"""

import sys
import thread
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from pimoteutils import *


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

thetext = "World"
number = 0
running = True
# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	global running
	global thetext
	#Override
	def buttonPressed(self, id, message):
		if id == b2.getId():
			running = False
			o.setText(thetext)
		elif id == b.getId():
			print("Toggle to: " + message)
		elif id == b3.getId():
			if message != "": 
				print(message)

# Create the phone object
thisphone = MyPhone()

b = ToggleButton("Hello", False)
b2 = Button("Yo")
b3 = InputText("Hello there")
o = OutputText("Hello")
#b.setValue(True);
thisphone.addButton(b)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addOutput(o)

#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)

myserver.start(ip, port)

#i want to get here ####################
print("got here")
