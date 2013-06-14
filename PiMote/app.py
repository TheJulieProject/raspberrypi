"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace

"""

import sys
# Import PhoneServer and Phone classes from pimoteutils
from pimoteutils import PhoneServer, Phone


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
class MyPhone(Phone):
  def buttonPressed(self, id):
    for button in Phone.buttons:
      if button.id == id:
        print(button.name) #Print the name of the button that was pressed

# Create the phone object
thisphone = MyPhone()


# Use the Phone method addButton(self, id, name) to add buttons
#    "id" - the ID you want the button to send back for parsing (int)
#    "name" - the name to be displayed on the button
thisphone.addButton(1, "This is button")
thisphone.addButton(2, "This is another")

#Create the server
myserver = PhoneServer()
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)
