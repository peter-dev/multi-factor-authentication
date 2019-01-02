from __future__ import division

import time
import os
import subprocess
import datetime

import picamera
import picamera.array
import numpy as np


class CaptureHandler:
	def __init__(self, camera, post_capture_callback=None):
		self.camera = camera
		self.callback = post_capture_callback
		self.detected = False
		self.working = False
		self.i = 0

	def motion_detected(self):
		if not self.working:
			self.detected = True

	def tick(self):
		if self.detected:
			print "Started working on capturing"
			self.working = True
			self.detected = False
			self.i += 1

			timestamp = datetime.datetime.now().isoformat()
			path = "captures/%s/" % timestamp
			filename = "spy_snap.jpg"
			output_file = path + filename

			os.makedirs(path)

			self.camera.start_preview()
			self.camera.capture(path + filename, use_video_port=True)    
			self.camera.stop_preview()

			print "Captured " + output_file

			if self.callback:
				self.callback(output_file, timestamp)

			self.working = False


class MyMotionDetector(picamera.array.PiMotionAnalysis):
	def __init__(self, camera, handler):
		super(MyMotionDetector, self).__init__(camera)
		self.handler = handler
		self.first = True

	def analyse(self, a):
		a = np.sqrt(
			np.square(a['x'].astype(np.float)) +
			np.square(a['y'].astype(np.float))
		).clip(0, 255).astype(np.uint8)
		if (a > 60).sum() > 50:
		# Ignore the first detection
			if self.first:
				self.first = False
				return
			self.handler.motion_detected()


class PiMotion:
	def __init__(self, verbose=False, post_capture_callback=None):
		self.verbose = verbose
		self.post_capture_callback = post_capture_callback

	def __print(self, str):
		if self.verbose:
			print str

	def start(self):
		with picamera.PiCamera() as camera:
			camera.resolution = (1280, 960)
			camera.framerate = 10
			# my camera is upside downand it needs to be rotated
			camera.rotation = 180 

			handler = CaptureHandler(camera, self.post_capture_callback)

			self.__print('Waiting 2 seconds for the camera to warm up')
			time.sleep(2)

			try:
				self.__print('Started recording')
				camera.start_recording(
					'/dev/null', format='h264',
					motion_output=MyMotionDetector(camera, handler)
				)

				while True:
					handler.tick()
					time.sleep(1)
			finally:
				camera.stop_recording()
				self.__print('Stopped recording')