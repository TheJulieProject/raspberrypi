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

class PhoneServer(Server):
	phone = None
	def addPhone(self, thephone):
		PhoneServer.phone = thephone
	def onStart(self):
		print("Server has started")
		
	def onMessage(self, socket, message):
		if PhoneServer.phone.controltype == Phone.NORMAL:
		# This function takes two arguments: 'socket' and 'message'.
		#     'socket' can be used to send a message string back over the wire.
		#     'message' holds the incoming message string (minus the line-return).
		#Currently, message holds the id of the button pressed
			(id, sep, msg) = message.strip().partition(",")
			PhoneServer.phone.buttonPressed(int(id), msg)
		elif PhoneServer.phone.controltype == Phone.CONTROLLER:
			print("Incoming")
			PhoneServer.phone.controlPress(int(message))
		
		# Signify all is well
		return True
	def onConnect(self, socket):
		print("Phone connected")
		if PhoneServer.phone.controltype == Phone.NORMAL:
			socket.send(str(PhoneServer.phone.controltype))
			for i in PhoneServer.phone.getButtons():
				socket.send(str(i.type) + "," + str(i.id) + "," + str(i.name))
		elif PhoneServer.phone.controltype == Phone.CONTROLLER:
			socket.send(str(PhoneServer.phone.controltype) + "," + str(PhoneServer.phone.pollrate))
		return True

	def onDisconnect(self, socket):
		print("Phone disconnected")
		return True


class Phone():
	NORMAL = 0
	CONTROLLER = 1
	buttons = []
	controltype = None
	pollrate = 5
	def __init__(self, type):
		self.controltype = type
	def addButton(self, type, id, name):
		if self.controltype == Phone.NORMAL:
			button = [""]
			button[0] = Button(type, id, name)
			Phone.buttons.append(button[0]);
		elif self.controltype == Phone.CONTROLLER:
			print("Can't add buttons to controller")
			sys.exit()
		return True
	def buttonPressed(self, id):
		pass
	def getButtons(self):
		return Phone.buttons
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
	def setPollRate(self, rate):
		Phone.pollrate = rate


class Button():
	id = None
	name = None
	type = None
	REGULAR = 1
	BUTTON_WITH_TEXT = 2
	TOGGLE_BUTTON = 3
	PRESET_CONTROL = 4
	def __init__(self, type, id, name):
		self.id = id
		self.name = name
		self.type = type
