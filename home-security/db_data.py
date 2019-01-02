# This script uses a lightweight query processing system (TinyDB) for storing and retrieving user information and logs
from tinydb import TinyDB, Query 
import time
# define db
dbUsers = TinyDB('db/users.json')
dbLogs = TinyDB('db/logs.json')
dbKeyPad = TinyDB('db/keypad.json')

def registerUsers():
	dbUsers.purge()
	dbUsers.insert({'keyId': '0008205542', 'accessCode': '1234', 'name': 'Piotr Baran'})
	dbUsers.insert({'keyId': '0008193407', 'accessCode': '5678', 'name': 'Tara Baran'})
	
def printUsers():
	print "List of all registered users: "
	for item in dbUsers:
		print(item)
		
def getUserByKeyId(keyId):
	user = Query()
	return dbUsers.get(user.keyId == keyId)
	
def createLogEntry(keyId, isRegistered = False, isAccessCodeValid = False):
	dbLogs.insert({'timestamp': time.time(), 'scannedKeyId': keyId, 'registered': isRegistered, 'authorised': isAccessCodeValid})

def storePersonalAccessCode(value):
	pac = Query()
	dbKeyPad.remove(pac.type == 'pac')
	dbKeyPad.insert({'timestamp': time.time(), 'type': 'pac', 'value': value})

def getPersonalAccessCode():
	pacRecord = Query()
	element = dbKeyPad.get(pacRecord.type == 'pac')
	if not element:
		return ""
	else:
		return element['value']
	
def setRequestPinStatus(value):
	status = Query()
	dbKeyPad.remove(status.type == 'status')
	dbKeyPad.insert({'timestamp': time.time(), 'type': 'status', 'value': value})

def getRequestPinStatus():
	statusRecord = Query()
	element = dbKeyPad.get(statusRecord.type == 'status')
	if not element:
		return False
	else:
		return element['value']

def resetKeyPadData():
	dbKeyPad.purge()
		