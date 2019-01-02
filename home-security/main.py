# This is the main script that triggers the application flow, the script peforms the following functions:
# - wait for rfid input, translate the input into text values and call authentication script
# - display feedback to the user using the LED Matrix array
#
# The HID character mapping is based on the following example
# https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100
#
#!/usr/bin/env python

import sys
import time
import db_data
import authentication
from sense_hat import SenseHat
sense = SenseHat()
# raspberry pi is rotated, hdmi port is on the right side
sense.set_rotation(90)

def displayAccessDenied():
	O = (255, 255, 255) # White
	X = (255, 0, 0) # Red
	sense.clear()
	
	noEntry = [
	O, O, X, X, X, X, O, O,
	O, X, O, O, O, O, X, O,
	X, O, O, O, O, O, O, X,
	X, O, X, X, X, X, O, X,
	X, O, X, X, X, X, O, X,
	X, O, O, O, O, O, O, X,
	O, X, O, O, O, O, X, O,
	O, O, X, X, X, X, O, O
	]
	
	sense.set_pixels(noEntry)
	time.sleep(5)
	sense.clear()
	
def displayAccessGranted():
	O = (255, 255, 255) # White
	X = (0, 255, 0) # Green
	sense.clear()
	
	entry = [
	O, O, X, X, X, X, O, O,
	O, X, O, O, O, O, X, O,
	X, O, O, X, X, O, O, X,
	X, O, X, X, X, X, O, X,
	X, O, X, X, X, X, O, X,
	X, O, O, X, X, O, O, X,
	O, X, O, O, O, O, X, O,
	O, O, X, X, X, X, O, O
	]
	
	sense.set_pixels(entry)
	time.sleep(10)
	sense.clear()

def displayEnterPac():
	sense.clear()
	sense.show_message("Enter PAC", text_colour=(0, 255, 0), back_colour=(0, 0, 0))
	sense.clear()

# HID character mapping (interested in digits from 0 to 9 only)
map = { 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0' }

# register predefined users
db_data.registerUsers()
db_data.printUsers()
# reset key pad data prior to start
db_data.resetKeyPadData()

scannedId = ""
done = False
# infinite loop
while True:
	f = open('/dev/hidraw0', 'rb')
	while not done:
		# read 8 characters from the input stream and translate one character at a time
		buffer = f.read(8)
		for c in buffer:
			if ord(c) > 0:
				# 40 is carriage return which signifies end of the scanned id
				if int(ord(c)) == 40:
					done = True
					break;
				# lookup mapping
				scannedId += map[ int(ord(c)) ]
	if scannedId:
		print "Scanned id: " + scannedId
		# execute authentication service before reading next input
		if authentication.validateKey(scannedId):
			# user found
			displayEnterPac()
			enteredPin = authentication.waitForPersonalAccessCode(scannedId)
			if enteredPin:
				isAuthorised = authentication.verifyPersonalAccessCode(scannedId, enteredPin)
				if isAuthorised:
					# success
					displayAccessGranted()
				else:
					# fail
					displayAccessDenied()
			else:
				# timeout, no pin provided
				displayAccessDenied()		
		else:
			# user not found
			displayAccessDenied()
		
		
	# reset to initial state and continue infinite loop
	f.close()
	scannedId = ""
	done = False
	
