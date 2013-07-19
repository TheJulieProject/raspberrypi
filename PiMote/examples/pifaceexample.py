import pifacedigitalio as p
from pimote import *

p.init()
pfd = p.PiFaceDigital()

class MyPhone(Phone):
	#Override
	def buttonPressed(self, id, message, phoneId):
		global pfd
		global buttons
		
		j = 0
		for j in range(0, 8):
			if buttons[j].getId() == id:
				self.changeLed(pfd, j, buttons[j])

	def changeLed(self, pfd, led, b):
		if b.getValue():
			pfd.leds[led].turn_on()
		else:
			pfd.leds[led].turn_off()

# Create the phone object
thisphone = MyPhone()
thisphone.setTitle("PiFace Control")

buttons = []

i=0
for i in range(0, 8):
	b = ToggleButton("Toggle LED " + str(i), False)
	buttons.append(b)
	thisphone.addButton(b)

#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start("0.0.0.0", 8090)