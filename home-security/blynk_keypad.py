# This script uses Blynk service to read Text input from the user (Mock interaction that replaces physical key pad)
# https://github.com/vshymanskyy/blynk-library-python
# 
# Run the script in the background: nohup python blynk_keypad.py &

import BlynkLib
import db_data

BLYNK_AUTH = 'BLYNK_AUTH_HERE'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# register virtual pin
@blynk.VIRTUAL_WRITE(1)
def v1_text_input_write_handler(value):
	print('Current V1 Text input: {}'.format(value))
	if db_data.getRequestPinStatus() == 'WAITING':
		db_data.storePersonalAccessCode(value)
		db_data.setRequestPinStatus('SUBMITTED')
		blynk.notify('Thank you for your PIN: ' + value)	

# register non blocking task running every 5 sec
def notify_to_enter_pin():
	if db_data.getRequestPinStatus() == 'PENDING':
		print "Requested Personal Access Code"
		db_data.setRequestPinStatus('WAITING')
		blynk.notify('Please enter your PIN')		

blynk.set_user_task(notify_to_enter_pin, 5000)
		
# start Blynk (this call should never return)	
blynk.run()	