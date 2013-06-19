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
	def buttonPressed(self, id, message):
		for button in Phone.buttons:
			if button.id == id:
				if button.type == button.REGULAR: #normal button
					print("'" + button.name + "'" + " button was pressed")
				elif button.type == button.INPUT_TEXT: #text input
					if message != "": #blank message means no text input + button press
						print(message)
				elif button.type == button.TOGGLE_BUTTON:
					print(button.name + " toggles to: " + message)

# Create the phone object
thisphone = MyPhone()

b = ToggleButton(1, "Hello World", False)
b2 = Button(2, "Yo")
b3 = InputText(3, "Hello there")
#b.setValue(True);
thisphone.addButton(b)
thisphone.addButton(b2)
thisphone.addButton(b3)

#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)
