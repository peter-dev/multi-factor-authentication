# This script uses Pi camera module to run motion detection and capture one picture when movement detected
#
# The motion detection application is based on the following project
# https://github.com/citrusbyte/pimotion

import requests
import json
from pimotion import PiMotion
"""
from wia import Wia
wia = Wia()
wia.access_token = "TOKEN_HERE"
"""

# enter your own slack webhook url
slackWebhookUrl = "URL_HERE"


def callbackWia(path, timestamp):
	"""
	print 'Uploading picture to Wia: ' + path
	# publish "photo-spy" event to Wia and the photo file 
	result = wia.Event.publish(name='photo-spy', file=open(path, 'rb'))
	"""

def callbackSlack(path, timestamp):
	print "Posting motification to slack with movement detected on " + timestamp
	payload = {"text": "Movement detected on " + timestamp + "\nDue to Wia issue, live preview is not available."}
	response = requests.post(slackWebhookUrl, data=json.dumps(payload), headers={"Content-type": "application/json"})
	print "Slack API Response:"
	print(response.text) #TEXT/HTML
	print(response.status_code, response.reason) #HTTP

motion = PiMotion(verbose=True, post_capture_callback=callbackSlack)
motion.start()