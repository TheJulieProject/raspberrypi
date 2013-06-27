#############################################
#											#
#			RANDOM KEY GENERATOR			#				
#											#
#			- some description -			#
#											#
#############################################


import string
import random


def generator(size, chars):
	return ''.join(random.choice(chars) for x in range(size))


size = 16
chars = string.ascii_letters + string.digits + "                    "

privateKey = "####################\n"

for x in range(0,30):
	privateKey += "# "
	privateKey += generator(size, chars)
	privateKey += " #\n"

privateKey += "####################\n"

print privateKey