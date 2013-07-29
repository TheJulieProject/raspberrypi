import Tkinter as tk
import pimote as pm


master = tk.Tk()
master.wm_title("PiMote Program Generator")
default_head = "from pimote import *\n\nclass MyPhone(Phone):\n\t#########----------------------------------------------###########\n\t"
default_head += "# Your code will go here! Check for the ID of the button pressed #\n\t# and handle that button press as you wish.                      #\n\t"
default_head += "#########----------------------------------------------###########\n\tdef buttonPressed(self, id, message, phoneId):\n"

notice = "This program is still a very early build. No validation has been added to the fields, so be careful with input!"

def nameExists(name):
	for c in components:
		if c[1] == name:
			return True
	return False
def add_new_button():
	name = "button_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([0, name, "Button"])
	print(name)
	refresh_layout()
def add_new_toggle():
	name = "toggle_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([1, name, "Toggle button", False])
	print(name)
	refresh_layout()
def add_new_input():
	name = "input_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([2, name, "Input Text"])
	print(name)
	refresh_layout()
def add_new_voice():
	name = "voice_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([3, name])
	print(name)
	refresh_layout()
def add_new_recurring():
	name = "recurring_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([4, name, 1000])
	print(name)
	refresh_layout()
def add_new_output():
	name = "output_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([5, name, "Output Field"])
	print(name)
	refresh_layout()
def add_new_progress():
	name = "progress_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([6, name, 100])
	print(name)
	refresh_layout()
def add_new_video():
	name = "video_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	# b = pm.VideoFeed(640, 480)
	# components.append([7, name, "0.0.0.0"])
	# print(name)
	# refresh_layout()
def add_new_spacer():
	name = "spacer_"
	num=1
	while nameExists(name+str(num)):
		num+=1
	name = name+str(num)
	components.append([8, name, 50])
	print(name)
	refresh_layout()

def refresh_layout():
	global inner_frame
	global layout_frame
	try:
		inner_frame.destroy()
	except Exception, e:
		print("Problem when destroying, " + str(e))
	inner_frame = tk.Frame(master=layout_frame)
	inner_frame.grid(row=1, column=2, rowspan=10, sticky=tk.N+tk.S+tk.W+tk.E)
	row = 0
	for c in components:
		comp_label = tk.Button(master=inner_frame, text=c[1], command= lambda c=c: show_properties(c))
		comp_label.grid(row=row, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
		row += 1

def show_properties(comp):
	print("Called: " + str(comp[0]))
	global properties_frame
	global properties_inner
	
	try:
		properties_inner.destroy()
	except:
		pass
	properties_inner = tk.Frame(master=properties_frame)
	properties_inner.grid(row=0, column=0, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)

	if comp[0] == 0:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Name: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=name_entry.get()))
		save_button.grid(row=2, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)
	elif comp[0] == 1:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Name: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		selected = tk.BooleanVar()
		selected_box = tk.Checkbutton(master=properties_inner, text="Initial Value", variable=selected, onvalue=True, offvalue=False)
		selected.set(comp[3])
		selected_box.grid(row=2, column=1)
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=name_entry.get(), initial_value=selected.get()))
		save_button.grid(row=3, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=3, column=0)
	elif comp[0] == 2:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Name: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=name_entry.get()))
		save_button.grid(row=2, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)
	elif comp[0] == 3:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="No properties for Voice Input").grid(row=1, column=0)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)
	elif comp[0] == 4:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Time Period: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=int(name_entry.get())))
		save_button.grid(row=2, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)
	elif comp[0] == 5:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Initial Text: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=name_entry.get()))
		save_button.grid(row=2, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)
	elif comp[0] == 6:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Max Value: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=int(name_entry.get())))
		save_button.grid(row=2, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)
	elif comp[0] == 7:
		pass
	elif comp[0] == 8:
		variable_name_label = tk.Label(master=properties_inner, text="Variable name: "+comp[1], anchor=tk.W, height=2).grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		name_label = tk.Label(master=properties_inner, text="Height: ").grid(row=1, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=1, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, value=int(name_entry.get())))
		save_button.grid(row=2, column = 1)
		delete_button = tk.Button(master=properties_inner, text="Delete", command=lambda:delete_component(comp=comp)).grid(row=2, column=0)

def save_component(comp = None, value="", initial_value=None):
	global info_label
	if comp[0] == 0 or comp[0] == 2 or comp[0] == 4 or comp[0] == 5 or comp[0] == 6 or comp[0] == 8:
		comp[2] = value
		info_label.config(text="Saved '" + comp[1] + "' {Value: " + str(comp[2])+"}")
	elif comp[0] == 1:
		comp[2] = value
		if initial_value == 1:
			comp[3] = True
		else:
			comp[3] = False
		info_label.config(text="Saved '" + comp[1] + "' {Value: " + str(comp[2])+", Initial Value: "+str(comp[3])+"}")
def delete_component(comp = None):
	global info_label
	global properties_inner
	global properties_frame
	info_label.config(text="Deleted '" + comp[1]+"'")
	components.remove(comp)
	refresh_layout()

	try:
		properties_inner.destroy()
	except:
		pass
	properties_inner = tk.Frame(master=properties_frame)
	properties_inner.grid(row=0, column=0, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)

def generate_program():
	my_program = open("myprogram.py", "w+")
	my_program.write(default_head)
	for c in components:
		my_program.write("\t\tif id == " + c[1] + ".getId():\n\t\t\tpass\n")
	my_program.write("\nphone = MyPhone()   # The phone object\n\n")
	for c in components:
		if c[0] == 0:
			my_program.write(c[1] + " = Button('"+c[2]+"')\nphone.add("+c[1]+")\n")
		elif c[0] == 1:
			my_program.write(c[1] + " = ToggleButton('"+c[2]+"', "+str(c[3])+")\nphone.add("+c[1]+")\n\n")
		elif c[0] == 2:
			my_program.write(c[1] + " = InputText('"+c[2]+"')\nphone.add("+c[1]+")\n\n")
		elif c[0] == 3:
			my_program.write(c[1] + " = VoiceInput()\nphone.add("+c[1]+")\n\n")
		elif c[0] == 4:
			my_program.write(c[1] + " = RecurringInfo("+str(c[2])+")\nphone.add("+c[1]+")\n\n")
		elif c[0] == 5:
			my_program.write(c[1] + " = OutputText('"+c[2]+"')\nphone.add("+c[1]+")\n\n")
		elif c[0] == 6:
			my_program.write(c[1] + " = ProgressBar("+str(c[2])+")\nphone.add("+c[1]+")\n\n")
		elif c[0] == 7:
			my_program.write(c[1] + " = VideoFeed("+c[2]+")\nphone.add("+c[1]+")\n\n")
		elif c[0] == 8:
			my_program.write(c[1] + " = Spacer("+str(c[2])+")\nphone.add("+c[1]+")\n\n")
	my_program.write("server = PhoneServer()\nserver.addPhone(phone)\nserver.start('0.0.0.0', 8090)")

	info_label.config(text="Generated program, saved as myprogram.py. To run type python myprogram.py into a terminal.")





	

components = []

main_frame = tk.Frame(master)
main_frame.grid(row=0, column=0)

info_label = tk.Label(master, text=notice, anchor=tk.W, height=5)
info_label.grid(row=1, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

buttons_label = tk.Label(master=main_frame, text="Add Components", height=3).grid(row=0, column=0)
add_button = tk.Button(master=main_frame, text="Add Button", command=add_new_button)
add_button.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_toggle = tk.Button(master=main_frame, text="Add Toggle Button", command=add_new_toggle)
add_toggle.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_input = tk.Button(master=main_frame, text="Add Text Input", command=add_new_input)
add_input.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_voice = tk.Button(master=main_frame, text="Add Voice Input", command=add_new_voice)
add_voice.grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_recurring = tk.Button(master=main_frame, text="Add poll", command=add_new_recurring)
add_recurring.grid(row=5, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_output = tk.Button(master=main_frame, text="Add Output Text", command=add_new_output)
add_output.grid(row=6, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_progress = tk.Button(master=main_frame, text="Add Progress Bar", command=add_new_progress)
add_progress.grid(row=7, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_video = tk.Button(master=main_frame, text="Add Video Feed", command=add_new_video)
add_video.grid(row=8, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_spacer = tk.Button(master=main_frame, text="Add Space", command=add_new_spacer)
add_spacer.grid(row=9, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

space = tk.Label(master=main_frame, width=10).grid(row=0, column=1)

layout_label = tk.Label(master=main_frame, text="Phone Layout").grid(row=0, column=2)
layout_frame = tk.Frame(master=main_frame)
layout_frame.grid(row=1, column=2, rowspan=10, sticky=tk.N+tk.S+tk.W+tk.E)
inner_frame = tk.Frame(master=layout_frame)
inner_frame.grid(row=0, column=0, rowspan=10, sticky=tk.N+tk.S+tk.W+tk.E)

space2 = tk.Label(master=main_frame, width=10, height=3).grid(row=0, column=3)

properties_label = tk.Label(master=main_frame, text="Properties", width=35).grid(row=0, column=4)
properties_frame = tk.Frame(master=main_frame)
properties_frame.grid(row=1, column=4, rowspan=99, sticky=tk.N+tk.S+tk.W+tk.E)
properties_inner = tk.Frame(master=properties_frame)
properties_inner.grid(row=0, column=0, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)

space3 = tk.Label(master=main_frame, width=10, height=3).grid(row=0, column=5)

server_label = tk.Label(master=main_frame, text="Server Controls").grid(row=0, column=6)
start_server = tk.Button(master=main_frame, text="Generate Program", command=generate_program)
start_server.grid(row=1, column=6, sticky=tk.N+tk.S+tk.W+tk.E)
# stop_server = tk.Button(master, text="Stop server", state="disabled")
# stop_server.grid(row=2, column=6, sticky=tk.N+tk.S+tk.W+tk.E)

space4 = tk.Label(master=main_frame, width=10, height=3).grid(row=0, column=7)

tk.mainloop()
