from pimote import *
import pifacedigitalio as p
import random, time, threading

#Initialize the PiFace
p.init()
pfd = p.PiFaceDigital()

# Variables to be used globally
started = False 		# Has the game begun
pattern = []			# The current pattern in the game
position = 0			# Where the user is up to with the input
sleeping = False		# Whether to accept input

class MyPhone(Phone):
	def buttonPressed(self, id, message, phoneId):
		# Declare global for access in this method
		global started
		global pattern
		global position
		global sleeping

		# If the game has not started, and we are accepting input
		if not started and not sleeping:
			started = True 								# Start
			pattern.append(random.randint(0, 3))		# Add a new random number to the pattern
			sleeping = True								# Stop accepting input
			t1 = threading.Thread(target=flashLeds)		# Flash the LED pattern
			t1.start()
		# If the game has begun, and we're accepting input
		elif not sleeping:							
			if id == b1.getId() and pattern[position] == 0:
				position += 1							# Correct in the pattern
			elif id == b2.getId() and pattern[position] == 1:
				position += 1							# Correct in the pattern
			elif id == b3.getId() and pattern[position] == 2:
				position += 1							# Correct in the pattern
			elif id == b4.getId() and pattern[position] == 3:
				position += 1							# Correct in the pattern
			else:		# They got the pattern wrong
				o.setText("Incorrect! You reached level " + str(len(pattern))+".&/Press any button to start again")
				self.reset()			# Reset the game

			# If we reached the end of the pattern
			if position == len(pattern) and started:
				pattern.append(random.randint(0,3))		# Add a new random number to the pattern
				position = 0							# Wait for the whole input again
				sleeping = True							# Stop accepting input
				o.setText("Watch")						# Visual indicator
				t1 = threading.Thread(target=flashLeds)	# Flash the pattern
				t1.start()

	# Used to reset all variables
	def reset(self):
		global position
		global pattern
		global started
		position = 0
		pattern = []
		started = False

# Flash the LED's in the correct pattern
def flashLeds():
	global sleeping
	n = 0 						# So we know when we're on the last one
	for i in pattern:			# Loop through the pattern
		pfd.leds[i].turn_on()	# Switch the LED on
		time.sleep(1)			# Sleep for 1 second
		pfd.leds[i].turn_off()	# Switch the LED off
		if n != len(pattern)-1:	# Check if we are at the end
			time.sleep(1)		# If we're not at the end, sleep for 1 second
		n+=1			
	sleeping = False			# We now accept input
	o.setText("Input the pattern!")		# Visual indicator


# Setting up the phone
thisphone = MyPhone()
thisphone.setTitle("Simons Game")	# Title to be displayed on the phone

# Add the buttons and output
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

# Create the server
server = PhoneServer()
setver.setMaxClients(1)				# Max clients that can connect
server.addPhone(thisphone)			# Add the phone to the server
# Start the server
server.start("0.0.0.0", 8090)