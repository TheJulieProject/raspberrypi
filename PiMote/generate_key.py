#################################################
#						#
#		RANDOM KEY GENERATOR		#				
#						#
#		- some description -		#
#						#
#################################################


import string
import random


def generator(size, chars):
	return ''.join(random.choice(chars) for x in range(size))


size = 16
chars = string.ascii_letters + string.digits + "                    "

privateKey = "#"

for x in range(0,30):
	privateKey += generator(size, chars)

privateKey += "#"

file = open('privatekey.data', 'w')
file.write(privateKey)

