import pifacedigitalio as p
from pimote import *

p.init()
pfd = p.PiFaceDigital()

ip = "0.0.0.0"
port = 8090

class MyPhone(Phone):
	#Override
	def buttonPressed(self, id, message, phoneId):
		global pfd
		#########----------------------------------------------###########
		# Your code will go here! Check for the ID of the button pressed #
		# and handle that button press as you wish.                      #
		#########----------------------------------------------###########
		if id == b.getId():
			if b.getValue():
				pfd.leds[0].turn_on()
			else:
				pfd.leds[0].turn_off()

# Create the phone object
thisphone = MyPhone()
thisphone.setTitle("PiFace Control")

b = ToggleButton("Toggle LED", False)
thisphone.addButton(b)

#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)