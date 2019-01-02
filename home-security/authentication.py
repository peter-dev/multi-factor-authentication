# This script is responsible for validating keyfob id, verifying personal access code and generating logs

import time
import db_data

# method takes one argument - scanned key id and checks if key is registered in the system	
def validateKey(scannedKeyId):
	userFound = db_data.getUserByKeyId(scannedKeyId)
	# check if key id exist in db
	if not userFound:
		print "Id not registered, creating log entry..."
		db_data.createLogEntry(scannedKeyId, False)
		db_data.setRequestPinStatus('CANCELED')
		return False
	else:
		db_data.setRequestPinStatus('PENDING')
		return True

		
# method waits 20 s for user to enter the pin number		
def waitForPersonalAccessCode(scannedKeyId):
	# wait 20 sec for user access code and terminate the flow
	seconds = 0
	enteredPin = ""
	while enteredPin == "":
		if seconds > 20:
			print "Reached max seconds, creating log entry..."
			db_data.createLogEntry(scannedKeyId, True, False)
			db_data.setRequestPinStatus('CANCELED')
			return False
		else:	
			if db_data.getRequestPinStatus() == 'SUBMITTED':
				enteredPin = db_data.getPersonalAccessCode()
				print "Retrieved pin code from db: " + enteredPin
				return enteredPin
		# wait 5 sec and continue
		time.sleep(5)
		seconds = seconds + 5

# method takes two arguments - scanned key id, and entered PIN	
def verifyPersonalAccessCode(scannedKeyId, personalAccessCode):
	print "PIN AUTHENTICATION RESULT"
	userFound = db_data.getUserByKeyId(scannedKeyId)
	enteredPin = db_data.getPersonalAccessCode()
	if userFound['accessCode'] == enteredPin:
		print "Matching access code: " + userFound['accessCode'] + " = " + enteredPin
		db_data.createLogEntry(scannedKeyId, True, True)
		return True
	else:
		print "No matching access code: " + userFound['accessCode'] +  " != " + enteredPin
		db_data.createLogEntry(scannedKeyId, True, False)
		return False
	
