import sys
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
        print(button.name)

# Create the phone object
thisphone = MyPhone()
# Use the Phone method addButton(self, id, name) to add buttons
#    "id" - the ID you want the button to send back for parsing (int)
#    "name" - the name to be displayed on the button
thisphone.addButton(1, "This is button")
thisphone.addButton(2, "This is another")
thisphone.addButton(3, "And another?!")
thisphone.addButton(4, "This is getting silly..")
thisphone.addButton(5, "Hello world")

myserver = PhoneServer()
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)
