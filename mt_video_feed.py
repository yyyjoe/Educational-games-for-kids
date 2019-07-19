# import the necessary packages
import datetime
from threading import Thread
import cv2
import numpy as np
import time
import copy

class FPS:
	def __init__(self):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0

	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self

	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()

	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1

	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()

	def fps(self):
		# compute the (approximate) frames per second
		return self._numFrames / self.elapsed()


class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True





class VideoFeed(object):
	def __init__(self, model):
		self.stream = WebcamVideoStream(src = 0).start()
		self.model = model
		
		# ROI properties
		self.x0, self.y0 = 50, 120
		self.x1, self.y1 = 850, 120
		self.width = 375
		self.dataColor = (255, 0, 0)

		self.classes = 'NONE ONE TWO THREE FOUR FIVE'.split()
		self.img_size = 64

		# Right ROI
		self.roi1 = None
		self.prediction1 = "NONE"
		Thread(target = self.fingerPrediction, args = (1,)).start()

		# Left ROI
		self.roi2 = None
		self.prediction2 = "NONE"
		Thread(target = self.fingerPrediction, args = (2,)).start()

		# Fonts
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.fx0, self.fy0 = 169, 15
		self.fx1, self.fy1 = 950, 15
		self.fh = 45


	def __del__(self):
		self.stream.stop()

	def binaryMask(self, img):
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.GaussianBlur(img, (7,7), 3)
		img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

		return img
	

	def fingerPrediction(self, which_roi):
		while True:
			if which_roi == 1:
				roi = self.roi1
			elif which_roi == 2:
				roi = self.roi2
			if not roi is None:
				roi = self.binaryMask(roi)
				roi = cv2.resize(roi, (self.img_size, self.img_size))
				img = np.float32(roi) / 255.
				img = np.expand_dims(img, axis = 0)
				img = np.expand_dims(img, axis = -1)
				if which_roi == 1:
					self.prediction1 = self.classes[np.argmax(self.model.predict(img)[0])]
				elif which_roi == 2:
					self.prediction2 = self.classes[np.argmax(self.model.predict(img)[0])]
				roi = None

	def get_frame(self):
		frame = self.stream.read()
		frame = cv2.flip(frame, 1)

		cv2.rectangle(frame, (self.x0,self.y0), (self.x0+self.width-1,self.y0+self.width-1), self.dataColor, 1)
		cv2.rectangle(frame, (self.x1,self.y1), (self.x1+self.width-1,self.y1+self.width-1), self.dataColor, 1)

		self.roi1 = frame[self.y0:self.y0+self.width,self.x0:self.x0+self.width]
		self.roi2 = frame[self.y1:self.y1+self.width,self.x1:self.x1+self.width]

		#cv2.putText(frame, "Left: {0}".format(self.prediction1), (self.fx0, self.fy0+2*self.fh), self.font, 1.0, (0,0,0), 3, 1)
		#cv2.putText(frame, "Right: {0}".format(self.prediction2), (self.fx1, self.fy1+2*self.fh), self.font, 1.0, (0,0,0), 3, 1)
		_, jpeg = cv2.imencode(".jpg", frame)
		return frame,jpeg.tobytes()


	def get_prediction(self):
		return self.prediction1, self.prediction2

