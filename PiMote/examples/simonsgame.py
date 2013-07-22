from pimote import *
import pifacedigitalio as p
import random, time, threading

p.init()
pfd = p.PiFaceDigital()

started = False
pattern = []
position = 0
sleeping = False

class MyPhone(Phone):
	def buttonPressed(self, id, message, phoneId):
		global started
		global pattern
		global position
		global sleeping

		if not started and not sleeping:
			started = True
			pattern.append(random.randint(0, 3))
			sleeping = True
			t1 = threading.Thread(target=flashLeds)
			t1.start()
		elif not sleeping:
			if id == b1.getId() and pattern[position] == 0:
				position += 1
			elif id == b2.getId() and pattern[position] == 1:
				position += 1
			elif id == b3.getId() and pattern[position] == 2:
				position += 1
			elif id == b4.getId() and pattern[position] == 3:
				position += 1
			else:
				o.setText("Incorrect! You reached level " + str(len(pattern))+".&/Press any button to start again")
				self.reset()

			if position == len(pattern) and started:
				pattern.append(random.randint(0,3))
				position = 0
				sleeping = True
				o.setText("Watch")
				t1 = threading.Thread(target=flashLeds)
				t1.start()
	def reset(self):
		global position
		global pattern
		global started
		position = 0
		pattern = []
		started = False

def flashLeds():
	global sleeping
	n = 0
	for i in pattern:
		pfd.leds[i].turn_on()
		time.sleep(1)
		pfd.leds[i].turn_off()
		if n != len(pattern)-1:
			time.sleep(1)
		n+=1			
	sleeping = False
	o.setText("Input the pattern!")

thisphone = MyPhone()

b1 = Button("LED 0")
b2 = Button("LED 1")
b3 = Button("LED 2")
b4 = Button("LED 3")
o = OutputText("Press any button to start")

thisphone.addButton(b1)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addButton(b4)
thisphone.addOutput(o)

server = PhoneServer()
server.addPhone(thisphone)

server.start("0.0.0.0", 8090)
