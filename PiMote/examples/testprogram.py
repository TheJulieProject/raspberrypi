"""
An example application using pimote
To run: python testprogram.py
  this will run it on ip=0.0.0.0 port=8090

Needs porting into python3 for use with the PiFace interface

"""

import sys, random
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from pimote import *

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	#Override
	buttonPress = 0
	def buttonPressed(self, id, message, phoneId):
		#########----------------------------------------------###########
		# Your code will go here! Check for the ID of the button pressed #
		# and handle that button press as you wish.                      #
		#########----------------------------------------------###########
		if id == b1.getId():
			self.buttonPress+=1
			o1.setText("<font color=#CC0000><b>Regular Button</b></font>: you have pressed it " + str(self.buttonPress) + " times")
		elif id == b2.getId():
			o2.setText("<font color=#CC0000><b>Toggle Button</b></font>: " + message)
		elif id == b3.getId():
			o3.setText("<font color=#CC0000><b>Input Text</b></font>: '" + message + "'")
		elif id == r.getId():
			i = random.randint(0, 100)
			p.setProgress(i)
			o4.setText("<font color=#CC0000><b>Progress Bar</b></font>: <b>"+str(i)+"</b>%")
		elif id == vi.getId():
			o5.setText("<font color=#CC0000><b>Voice Input</b></font>: '" + message + "'")

# Create the phone object
thisphone = MyPhone()
thisphone.setTitle("Example PiMote App")
p = ProgressBar(100)
b1 = Button("Hello") #Regular button
b2 = ToggleButton("This is a toggle button", True) #Toggle
b3 = InputText("Input text here") #Text Input
title = OutputText("<div align='center'><font color=#35B5E5 font-size=25px><b>Test Application</b></font></div>")
title.setTextSize(20)
o = OutputText("This is a <i>test</i> application, controlling an RPi from and Android phone!"
			   + "<br>It's really simple! And using the <b>HTML</b> markup, you can make it look really classy!")
o1 = OutputText("<font color=#CC0000><b>Regular Button</b></font>:")
o2 = OutputText("<font color=#CC0000><b>Toggle Button</b></font>:") #Output field
o3 = OutputText("<font color=#CC0000><b>Input Text</b></font>:")
o4 = OutputText("<font color=#CC0000><b>Progress Bar</b></font>:")
o5 = OutputText("<font color=#CC0000><b>Voice Input</b></font>:")
o6 = OutputText("This is refreshing due to a <font color=#CC0000><b>RecurringInfo</b></font> which 'polls' the phone. It's like pressing a button over and over!")
o7 = OutputText("<font color=#CC0000>Video Feed</font>")
v = VideoFeed(640, 480) #Live video feed
vi = VoiceInput() #Voice input
s = Spacer(100)
r = RecurringInfo(2000)

#Add the buttons to the phone
thisphone.addOutput(title)
thisphone.addOutput(o)
thisphone.addSpace(s)
thisphone.addOutput(o1)
thisphone.addButton(b1)
thisphone.addSpace(s)
thisphone.addOutput(o2)
thisphone.addButton(b2)
thisphone.addSpace(s)
thisphone.addOutput(o3)
thisphone.addButton(b3)
thisphone.addSpace(s)
thisphone.addOutput(o4)
thisphone.addOutput(p)
thisphone.addButton(r)
thisphone.addOutput(o6)
thisphone.addSpace(s)
thisphone.addOutput(o5)
thisphone.addButton(vi)
#thisphone.addSpace(s)
#thisphone.addOutput(o7)
#thisphone.addVideoFeed(v)

#Create the server
myserver = PhoneServer()
myserver.setPassword("helloworld")
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start("0.0.0.0", 8090)
