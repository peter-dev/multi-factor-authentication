# Installation Guide

This guide will explain how to set up the Raspberry PI to run the multi-factor security application.

## Hardware requirements

### Sense Hat

- Attach a Sense HAT add-on board to the Pi. Follow the instructions [here](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/3)
- Install a software package on the Raspberry Pi:
  ```
  $ sudo apt update
  $ sudo apt upgrade
  $ sudo apt install sense-hat
  ```

### Raspberry Pi Camera

- Connect a Pi camera module to the Pi. Follow the instuctions [here](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/4)
- Open a terminal window on the RPi and enter the following  command:
  ```
  $ sudo raspi-config
  ```
- Select option `5 Interfacing Options`
- Select `P1 Camera` and enable the camera interface
- Exit raspi-conf by selecting `back/exit`
- Reboot your device
- We can check the camera status from the terminal, enter the following command:
  ```
  $ vcgencmd get_camera
  ```

### Proximity Sensor ID Card Reader with USB Interface

- I used the following Proximity Sensor ID Card Reader from [Amazon](https://www.amazon.co.uk/gp/product/B018TXQWRE/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)
- The reader is registered as HID device on the Raspberry Pi. 
- Add the following line to dev rules in `/etc/udev/rules.d/` in order to access the input stream without sudo command
  ```
  KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"
  ```

## Software requirements

### Blynk

- Install a [python based Blynk library](https://github.com/vshymanskyy/blynk-library-python) on the Raspberry Pi
  ```
  $ pip install blynk-library-python
  ```
- Install the Blynk App for your Smartphone (or Tablet) from [here](https://www.blynk.cc/getting-started/)
- Create a new account in Blynk App
- Create a new project and select `Raspberry Pi 3` as the board
- Add `Notification` widget to the project
- Add `Text Input` widget and call it "KeyPad (Mock)"
- Select Virtual Pin 1 `V1` as output and set Character Limit to `4`
- Your Blynk Auth Token will be required in the `blynk_keypad.py` script

### Wia

- Create an account on [Wia.io](https://www.wia.io/)
- Install Wia on the Raspberry Pi
  ```
  $ pip install wia
  ```
- Go to the Wia Dashboard and select `Create a New Space` then select `Devices`
- Add a device and give it the name "SensePi"
- Now, in the Configuration tab for your device, you will find device_secret_key which should begin with d_sk
- Your Wia Access Token will be required in the `home-spy` application [line 12]

### TinyDB

- Install a JSON-based database on the Raspberry Pi
  ```
  $ pip install TinyDB
  ```

### Slack

- Follow the [offical guide](https://api.slack.com/incoming-webhooks) to enable Incoming Webhooks feature
- Your Webhook URL will be required in the `home-spy` application [line 16]
