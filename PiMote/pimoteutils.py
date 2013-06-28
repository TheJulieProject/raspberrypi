"""

ex3.py - Module for ex3 - David Thorne / AIG / 15-01-2009 
Renamed and used as pimoteutils by Tom Richardson - 14/06/2013 


"""

import sys
import threading
import time
import socket as socketlib
import subprocess


class Socket():
	"""
	Mutable wrapper class for sockets.
	"""

	def __init__(self, socket):
		# Store internal socket pointer
		self._socket = socket
	
	def send(self, msg):
		# Ensure a single new-line after the message
		self._socket.send("%s\n" % msg.strip())
		
	def close(self):
		self._socket.close()
		

class Receiver():
	"""
	A class for receiving newline delimited text commands on a socket.
	"""

	def __init__(self):
		# Protect access
		self._lock = threading.RLock()
		self._running = True

	def __call__(self, socket):
		"""Called for a connection."""
		# Set timeout on socket operations
		socket.settimeout(1)

		# Wrap socket for events
		wrappedSocket = Socket(socket)
		
		# Store the unprocessed data
		stored = ''
		chunk = ''
		
		# On connect!
		self._lock.acquire()
		self.onConnect(wrappedSocket)
		self._lock.release()
		
		# Loop so long as the receiver is still running
		while self.isRunning():
		
			# Take everything up to the first newline of the stored data
			(message, sep, rest) = stored.partition('\n')
			if sep == '': # If no newline is found, store more data...
				while self.isRunning():
					try:
						chunk = ''
						chunk = socket.recv(1024)
						stored += chunk
						break
					except socketlib.timeout:
						pass
					except:
						print 'EXCEPTION'
				
				# Empty chunk means disconnect
				if chunk == '':
					break;

				continue
			else: # ...otherwise store the rest
				stored = rest			
				
			# Process the command
			self._lock.acquire()
			success = self.onMessage(wrappedSocket, message)
			self._lock.release()
			
			if not success:
				break;

		# On disconnect!
		self._lock.acquire()
		self.onDisconnect(wrappedSocket)		
		self._lock.release()
		socket.close()
		del socket
		
		# On join!
		self.onJoin()
			
	def stop(self):
		"""Stop this receiver."""
		self._lock.acquire()
		self._running = False
		self._lock.release()
		
	def isRunning(self):
		"""Is this receiver still running?"""
		self._lock.acquire()
		running = self._running
		self._lock.release()
		return running
		
	def onConnect(self, socket):
		pass

	def onMessage(self, socket, message):
		pass

	def onDisconnect(self, socket):
		pass

	def onJoin(self):
		pass

		
		
class Server(Receiver):

	def start(self, ip, port):
		# Set up server socket
		serversocket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
		serversocket.setsockopt(socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1)
		serversocket.bind((ip, int(port)))
		serversocket.listen(10)
		serversocket.settimeout(1)
		
		# On start!
		self.onStart()

		# Main connection loop
		threads = []
		while self.isRunning():
			try:
				(socket, address) = serversocket.accept()
				thread = threading.Thread(target = self, args = (socket,))
				threads.append(thread)
				thread.start()
			except socketlib.timeout:
				pass
			except:
				self.stop()

		# Wait for all threads
		while len(threads):
			threads.pop().join()

		# On stop!				
		self.onStop()

	def onStart(self):
		pass

	def onStop(self):
		pass



class Client(Receiver):
	
	def start(self, ip, port):
		# Set up server socket
		self._socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
		self._socket.settimeout(1)
		self._socket.connect((ip, int(port)))

		# On start!
		self.onStart()

		# Start listening for incoming messages
		self._thread = threading.Thread(target = self, args = (self._socket,))
		self._thread.start()
		
	def send(self, message):
		# Send message to server
		self._lock.acquire()
		self._socket.send("%s\n" % message.strip())
		self._lock.release()
		time.sleep(0.5)

	def stop(self):
		# Stop event loop
		Receiver.stop(self)
		
		# Join thread
		if self._thread != threading.currentThread():
			self._thread.join()
		
		# On stop!
		self.onStop()		

	def onStart(self):
		pass

	def onStop(self):
		pass
		
	def onJoin(self):
		self.stop()


########################-------SERVER-------########################################
#  This is the main server that runs on the pi. All messages are sorted here and sent
#  to the phone that handles them.
#  It also initialises and sorts the security.

class PhoneServer(Server):
	#Protocol final static variables
	SENT_PASSWORD = 0
	SENT_DATA = 1
	PASSWORD_FAIL = 2314
	REQUEST_PASSWORD = 9855
	STORE_KEY = 5649

	phone = None
	isPassword = False
	clientMax = False
	noOfClients = 0

	#Store the phone object for reference
	def addPhone(self, thephone): 
		self.phone = thephone

	#Called when the server is started
	def onStart(self):
		print("Server has started")
		if self.isPassword: #If password protected
			read = False
			while not read: #Loop to get the key
				try:
					file = open("privatekey.data", "r")
					self.key = file.read() #Read the key
					read = True
				except: #No such file so generate key and file
					subprocess.call("python generate_key.py", shell=True)

	#Called when a message is recieved from the phone
	def onMessage(self, socket, message):
		#First int is a protocol variable
		(sentType, sep, msg) = message.strip().partition(",")
		if int(sentType) == PhoneServer.SENT_PASSWORD: #Password data
			self.managePassword(msg, socket)
		elif int(sentType) == PhoneServer.SENT_DATA: #Input data
			self.manageIncomingMessage(msg)
		
		# Signify all is well
		return True

	#Called when a phone connects to the server
	def onConnect(self, socket):
		print("Phone connected")
		self.noOfClients+=1 #Counting clients
		if self.clientMax:
			if self.noOfClients > self.maxClients:
				socket.send(str(PhoneServer.PASSWORD_FAIL)) #Kick them if full

		if self.isPassword: #if the server has password, request it
			socket.send(str(PhoneServer.REQUEST_PASSWORD))
		else: #otherwise setup
			self.phone.setup(socket)
		return True

	#Called when a phone disconnects from the server
	def onDisconnect(self, socket):
		print("Phone disconnected")
		self.noOfClients-=1 #tracking clients
		return True

	#Used to set a password for the server
	def setPassword(self, pswd):
		self.isPassword = True
		self.password = pswd

	#Handle the password recieved from the phone
	def managePassword(self, password, socket):
		if password == self.password: #Password was right, tell them to store key
			socket.send(str(PhoneServer.STORE_KEY)+","+self.key)
			self.phone.setup(socket)#setup
		elif password == self.key:#they had a key
			self.phone.setup(socket)#setup
		else:#wrong password
			socket.send(str(PhoneServer.PASSWORD_FAIL)) #kick them

	#Manage incoming message
	def manageIncomingMessage(self, message):
		if isinstance(self.phone, Phone): #Regular phone
			(id, sep, msg) = message.strip().partition(",") #Strip component ID and message apart
			self.phone.updateButtons(int(id), msg) #Update buttons if needed
			self.phone.buttonPressed(int(id), msg) #Allow the user to handle the message
		elif isinstance(self.phone, ControllerPhone): #Controller
			self.phone.controlPress(message) #Controller handler

	#Used to limit the amount of clients that can connect at one time
	def setMaxClients(self, x):
		self.clientMax = True
		self.maxClients = x

################------PHONE TYPES--------####################

class Phone():
	buttons = [] #For user use
	outputs = []
	components = [] #To send to phone

	controltype = 0 #Type of phone

	video = False

	#More final protocol variables for setup
	INPUT_REGULAR = 1
	INPUT_TEXT = 2
	INPUT_TOGGLE = 3
	OUTPUT_TEXT = 4
	VIDEO_FEED = 5
	VOICE_INPUT = 6
	#Setup
	SET_CONTROL_TYPE = 0
	SETUP = 1
	#Data being sent
	REQUEST_OUTPUT_CHANGE = 2

	#Add a button to the phone
	def addButton(self, button):
		if isinstance(button, Button):
			button.id = len(self.buttons)
			self.buttons.append(button)
			self.components.append(button)
		else:
			print("Button not provided")

	#Add an output to the phone
	def addOutput(self, output):
		if isinstance(output, OutputText):
			output.id = len(self.outputs)
			self.outputs.append(output)
			self.components.append(output)
		else:
			print("Not an output")

	#Add a video feed to the phone
	def addVideoFeed(self, vid):
		if self.video:
			print("You can only have one video feed running..")
			sys.exit(0)
		else:
			self.vid = vid
			self.video = True
			self.components.append(vid)

	#User overrides this. Called when a message is recieved
	def buttonPressed(self, id, msg):
		pass
	#Returns all buttons
	def getButtons(self):
		return self.buttons
	#Returns all outputs
	def getOutputs(self):
		return self.outputs
	#Used for setup
	def setup(self, socket):
		self.socket = socket
		socket.send(str(Phone.SET_CONTROL_TYPE)+","+str(self.controltype))
		for c in self.components:
			c.setup(socket) #setup each component
	#Updates the state of buttons (toggle)
	def updateButtons(self, id, message):
		for b in self.buttons:
			if b.id == id:
				if isinstance(b, ToggleButton):
					value = False
					if(int(message) == 1):
						value = True
					b.setValue(value)
	


class ControllerPhone():
	controltype = 1
	video = False
	voice = False
	def controlPress(self, type):
		pass
	def setVideo(self, value):
		self.video = value
	def setVoice(self, value):
		self.voice = value
	def setup(self, socket):
		voiceV = videoV = 0
		if self.video == True:
			videoV = 1
		if self.voice == True:
			voiceV = 1
		socket.send(str(Phone.SET_CONTROL_TYPE)+","+str(self.controltype) + "," + str(videoV) + "," + str(voiceV))



####################----COMPONENTS----######################

class Button():
	def __init__(self, name):
		self.name = name
		self.type = Phone.INPUT_REGULAR
	def getId(self):
		return self.id
	def getName(self):
		return self.name
	def getType(self):
		return self.type
	def setup(self, socket):
		socket.send(str(Phone.SETUP)+","+str(self.type) + "," + str(self.id) + "," + str(self.name))

class InputText(Button):
	def __init__(self, name):
		self.name = name
		self.type = Phone.INPUT_TEXT
	def setup(self, socket):
		socket.send(str(Phone.SETUP)+","+str(self.type) + "," + str(self.id) + "," + str(self.name))

class ToggleButton(Button):
	def __init__(self, name, initialvalue):
		self.name = name
		self.value = initialvalue
		self.type = Phone.INPUT_TOGGLE
	def getValue(self):
		return self.value
	def setValue(self, value):
		self.value = value
	def setup(self, socket):
		tf = 0
		if self.value == True:
			tf=1
		socket.send(str(Phone.SETUP)+","+str(self.type) + "," + str(self.id) + "," + str(self.name) + "," + str(tf))

class VoiceInput(Button):
	def __init__(self):
		self.type = Phone.VOICE_INPUT
	def setup(self, socket):
		socket.send(str(Phone.SETUP)+","+str(self.type)+","+str(self.id))



class OutputText():
	message = ""
	def __init__(self, initialmessage):
		self.type = Phone.OUTPUT_TEXT
		self.message = initialmessage
	def setText(self, message):
		self.message = message
		self.socket.send(str(Phone.REQUEST_OUTPUT_CHANGE)+","+str(self.id)+","+str(self.message))
	def getText(self):
		return self.message
	def setup(self, socket):
		self.socket = socket
		socket.send(str(Phone.SETUP)+","+str(self.type)+","+str(self.id)+","+str(self.message)) 

class VideoFeed():
	outsidefeed = 0;
	ip = "-"
	def __init__(self, width, height):
		self.type = Phone.VIDEO_FEED
		self.width = width
		self.height = height
	def setIp(self, ip):
		self.ip = ip
		self.outsidefeed = 1
	def setup(self, socket):
		socket.send(str(Phone.SETUP)+","+str(self.type)+","+str(self.width)+","+str(self.height)+","+str(self.outsidefeed)+","+self.ip)