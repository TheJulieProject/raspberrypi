"""

ex3.py - Module for ex3 - David Thorne / AIG / 15-01-2009 
Renamed and used as pimoteutils by Tom Richardson - 14/06/2013 


"""

import sys
import threading
import time
import socket as socketlib


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


class PhoneServer(Server):
	SENT_PASSWORD = 0
	SENT_DATA = 1
	PASSWORD_FAIL = 2314
	REQUEST_PASSWORD = 9855
	STORE_KEY = 5649
	phone = None
	isPassword = False
	key = "thisistheserverkey1876"
	clientMax = False
	noOfClients = 0
	def addPhone(self, thephone):
		self.phone = thephone
	def onStart(self):
		print("Server has started")
		
	def onMessage(self, socket, message):
		(sentType, sep, msg) = message.strip().partition(",")
		if int(sentType) == PhoneServer.SENT_PASSWORD:
			self.managePassword(msg, socket)
		elif int(sentType) == PhoneServer.SENT_DATA:
			self.manageIncomingMessage(msg)
		
		# Signify all is well
		return True

	def onConnect(self, socket):
		print("Phone connected")
		self.noOfClients+=1
		if self.clientMax:
			if self.noOfClients > self.maxClients:
				socket.send(str(PhoneServer.PASSWORD_FAIL))

		if self.isPassword:
			socket.send(str(PhoneServer.REQUEST_PASSWORD))
		else:
			self.phone.setup(socket)
		return True

	def onDisconnect(self, socket):
		print("Phone disconnected")
		self.noOfClients-=1
		return True

	def setPassword(self, pswd):
		self.isPassword = True
		self.password = pswd

	def managePassword(self, password, socket):
		if password == self.password:
			socket.send(str(PhoneServer.STORE_KEY)+","+self.key)
			self.phone.setup(socket)
		elif password == self.key:
			self.phone.setup(socket)
		else:
			socket.send(str(PhoneServer.PASSWORD_FAIL))

	def manageIncomingMessage(self, message):
		if isinstance(self.phone, Phone):
			(id, sep, msg) = message.strip().partition(",")
			self.phone.updateButtons(int(id), msg)
			self.phone.buttonPressed(int(id), msg)
		elif isinstance(self.phone, ControllerPhone):
			self.phone.controlPress(message)

	def setMaxClients(self, x):
		self.clientMax = True
		self.maxClients = x

################------PHONE TYPES--------####################

class Phone():
	buttons = []
	outputs = []
	video = False
	controltype = 0
	INPUT_REGULAR = 1
	INPUT_TEXT = 2
	INPUT_TOGGLE = 3
	OUTPUT_TEXT = 4
	VIDEO_FEED = 5
	VOICE_INPUT = 6
	SET_CONTROL_TYPE = 0
	SETUP = 1
	REQUEST_OUTPUT_CHANGE = 2
	def addButton(self, button):
		if isinstance(button, Button):
			button.id = len(self.buttons)
			self.buttons.append(button)
		else:
			print("Button not provided")
	def addOutput(self, output):
		if isinstance(output, OutputText):
			output.id = len(self.outputs)
			self.outputs.append(output)
		else:
			print("Not an output")
	def addVideoFeed(self, vid):
		if self.video:
			print("You can only have one video feed running..")
			sys.exit(0)
		else:
			self.vid = vid
			self.video = True
	def buttonPressed(self, id, msg):
		pass
	def getButtons(self):
		return self.buttons
	def setup(self, socket):
		self.socket = socket
		socket.send(str(Phone.SET_CONTROL_TYPE)+","+str(self.controltype))
		for i in self.buttons:
			i.setup(socket)
		for o in self.outputs:
			o.socket = socket
			o.setup(socket)
		if self.video == True:
			self.vid.setup(socket)
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
		'''
		0 - Forward
		1 - Forward and left
		2 - Forward and right
		3 - Backwards
		4 - Backwards and left
		5 - Backwards and right
		6 - Right
		7 - Left
		'''
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