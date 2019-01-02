# A multi-factor authentication security system using Raspberry Pi

## A custom multi-factor security implementation that can be used to provide a secure door entry system at home or other building facilities.

### Sample happy scenario:

1. User place the key fob by the reader that sends the input to the device
2. Validation script running on the Pi talks to the database to see if key fob id is registered with the system
3. Upon successful validation user is prompted to enter PIN access code
4. Green colour lights up on the LED array and user has 5 seconds to open the door
   - electronic door strike is not physically available (this is a Mock interaction)

### Possible enhancements:

- motion detection, picture taken, notification sent when movement detected at the door (implemented)
- random access code sent as text message / email
- face recognition validation

### Tools, Technologies and Equipment:

- Raspberry Pi 3 Model B+	 - built in Wi-Fi used for communication with external services
- Sense Hat add-on - 8x8 LED matrix array displays alerts and confirmations to the user
- Raspberry Pi cam	 - takes picture of a person at the door (motion detection and face recognition enhancements possible)
- USB RFID reader	 - takes the code from RFID key fobs and cards and sends it to Raspberry Pi device
- Keypad (Mock)	 - using Blynk widget to enter PIN number associated with the registered user
- Lightweight DB	 - stores registered users along with key fob details and PIN numbers
- Messaging	 	 - Slack integration using Webhook API calls to enable instant notifications on smartphone or laptop


### Installation Steps:

https://github.com/peter-dev/multi-factor-authentication/docs/installation.md


