from pimote import *
import pifacedigitalio as p
import random, time

p.init()
pfd = p.PiFaceDigital()

started = False
pattern = []

class MyPhone(Phone):
	def messageReceived(self, id, message, phoneId):
		global started
		global pfd
		if not started:
			started = True
			pattern.append(random.randint(0, 3))
			for i in pattern:
				flashLed(i)
		else:
			pass

	def flashLed(self, led):
		pfd.leds[led].turnOn()
		time.sleep(1)
		pfd.leds[led].turnOff()
			


thisphone = MyPhone()

b1 = Button("LED 1")
b2 = Button("LED 2")
b3 = Button("LED 3")
b4 = Button("LED 4")

thisphone.addButton(b1)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addButton(b4)

server = PhoneServer()
server.addPhone(thisphone)

server.start("0.0.0.0", 8090)