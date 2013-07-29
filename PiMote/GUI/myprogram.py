from pimote import *
class MyPhone(Phone):
	#########----------------------------------------------###########
	# Your code will go here! Check for the ID of the button pressed #
	# and handle that button press as you wish.                      #
	#########----------------------------------------------###########
	def buttonPressed(self, id, message, phoneId):
		if id == button_1.getId():
			pass
		if id == toggle_1.getId():
			pass
		if id == input_1.getId():
			pass

phone = MyPhone()   # The phone object

button_1 = Button('Button')
phone.add(button_1)
toggle_1 = ToggleButton('Toggle button', False)
phone.add(toggle_1)

input_1 = InputText('Input Text')
phone.add(input_1)

server = PhoneServer()
server.addPhone(phone)
server.start('0.0.0.0', 8090)