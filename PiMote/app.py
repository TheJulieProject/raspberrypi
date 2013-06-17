"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace

"""

import sys
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from pimoteutils import PhoneServer, Phone, Button


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	#Override
	#def buttonPressed(self, id, message):
		#for button in Phone.buttons:
			#if button.id == id:
				#if button.type == button.REGULAR: #normal button
					#print("'" + button.name + "'" + " button was pressed")
				#elif button.type == button.BUTTON_WITH_TEXT: #text input
					#if message != "": #blank message means no text input + button press
						#print(message)
	def controlPress(self, type):
		print(str(type))

# Create the phone object
thisphone = MyPhone(Phone.CONTROLLER)


# Use the Phone method addButton(self, id, name) to add buttons
#    "id" - the ID you want the button to send back for parsing (int)
#    "name" - the name to be displayed on the button
#thisphone.addButton(Button.BUTTON_WITH_TEXT, 1, "This is a text field")
#thisphone.addButton(Button.REGULAR, 2, "This is another")
#thisphone.addButton(Button.BUTTON_WITH_TEXT, 3, "More text")

#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)
