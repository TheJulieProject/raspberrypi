from pimote import *
import sys
import time
import move_robot_with_hands as moveRobot

# ROBOT_CONTROL actions
LEFT_OFF 	= "1,0,0" 
LEFT_UP 	= "1,0,1"
LEFT_DOWN	= "1,0,3"

RIGHT_OFF 	= "1,0,4"
RIGHT_UP	= "1,0,5"
RIGHT_DOWN	= "1,0,7"

ip = sys.argv[1]
port = int(sys.argv[2])

running = False

class MyClient(Client):
  def onMessage(self, socket, message):
    print(message)
    return True
  def onConnect(self, socket):
    print("joined")
    setRunning(True)
    return True
  def onDisconnect(self, socket):
    print("disconnected")
    setRunning(False)
    return True

def setRunning(value):
  global running
  running = value

client = MyClient()
client.start(ip, port)

while(True):
 if running:        
 	try:
		#Get all the image processing information		
  		command = moveRobot.move()
  		
  		# Split the command into right and left motors.
  		commandRight, commandLeft = command.split("_")
		
  		if commandLeft == "1":
			print "LEFT_UP"
			client.send(LEFT_UP)
  		elif commandLeft == "-1":
			print "LEFT_DOWN"
			client.send(LEFT_DOWN)
  		elif commandLeft == "0":
			print "LEFT_OFF"
			client.send(LEFT_OFF)  		

  		if commandRight == "1":
			print "RIGHT_UP"
			client.send(RIGHT_UP)
  		elif commandRight == "-1":
			print "RIGHT_DOWN"
			client.send(RIGHT_DOWN)
  		elif commandRight == "0":
			print "RIGHT_OFF"
			client.send(RIGHT_OFF)	  
    
  	except:
    	 print("Error")
    	 running = False
    	 client.stop()
client.stop()
