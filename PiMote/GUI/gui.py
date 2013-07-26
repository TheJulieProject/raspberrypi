import Tkinter as tk
import pimote as pm


master = tk.Tk()

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
	inner_frame.grid(row=1, column=2, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)
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
		current_name = ""
		name_label = tk.Label(master=properties_inner, text="Name: ").grid(row=0, column=0)
		name_entry = tk.Entry(master=properties_inner)
		name_entry.grid(row=0, column=1)
		name_entry.insert(0, comp[2])
		save_button = tk.Button(master=properties_inner, text="Save", command=lambda:save_component(comp=comp, name=name_entry.get()))
		save_button.grid(row=1, column = 1)
		edit_pressed = tk.Button(master=properties_inner, text="Handle Press")
		edit_pressed.grid(row=1, column=0)
	elif comp[0] == 1:
		pass
	elif comp[0] == 2:
		pass
	elif comp[0] == 3:
		pass
	elif comp[0] == 4:
		pass
	elif comp[0] == 5:
		pass
	elif comp[0] == 6:
		pass
	elif comp[0] == 7:
		pass
	elif comp[0] == 8:
		pass

def save_component(comp = None, name=""):
	print("Saving name as " + name)
	if comp[0] == 0:
		comp[2] = name
	

components = []

buttons_label = tk.Label(master, text="Add Components", height=3).grid(row=0, column=0)
add_button = tk.Button(master, text="Add Button", command=add_new_button)
add_button.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_toggle = tk.Button(master, text="Add Toggle Button", command=add_new_toggle)
add_toggle.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_input = tk.Button(master, text="Add Text Input", command=add_new_input)
add_input.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_voice = tk.Button(master, text="Add Voice Input", command=add_new_voice)
add_voice.grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_recurring = tk.Button(master, text="Add poll", command=add_new_recurring)
add_recurring.grid(row=5, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_output = tk.Button(master, text="Add Output Text", command=add_new_output)
add_output.grid(row=6, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_progress = tk.Button(master, text="Add Progress Bar", command=add_new_progress)
add_progress.grid(row=7, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_video = tk.Button(master, text="Add Video Feed", command=add_new_video)
add_video.grid(row=8, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
add_spacer = tk.Button(master, text="Add Space", command=add_new_spacer)
add_spacer.grid(row=9, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

space = tk.Label(master, width=10).grid(row=0, column=1)

layout_label = tk.Label(master, text="Phone Layout").grid(row=0, column=2)
layout_frame = tk.Frame(master)
layout_frame.grid(row=1, column=2, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)
inner_frame = tk.Frame(master=layout_frame)
inner_frame.grid(row=0, column=0, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)

space2 = tk.Label(master, width=10, height=3).grid(row=0, column=3)

properties_label = tk.Label(master, text="Properties").grid(row=0, column=4)
properties_frame = tk.Frame(master)
properties_frame.grid(row=1, column=4, rowspan=99, sticky=tk.N+tk.S+tk.W+tk.E)
properties_inner = tk.Frame(master=properties_frame)
properties_inner.grid(row=0, column=0, rowspan=9, sticky=tk.N+tk.S+tk.W+tk.E)

space3 = tk.Label(master, width=10, height=3).grid(row=0, column=5)

server_label = tk.Label(master, text="Server Controls").grid(row=0, column=6)
start_server = tk.Button(master, text="Start server")
start_server.grid(row=1, column=6, sticky=tk.N+tk.S+tk.W+tk.E)
stop_server = tk.Button(master, text="Stop server", state="disabled")
stop_server.grid(row=2, column=6, sticky=tk.N+tk.S+tk.W+tk.E)

space4 = tk.Label(master, width=10, height=3).grid(row=0, column=7)

tk.mainloop()
