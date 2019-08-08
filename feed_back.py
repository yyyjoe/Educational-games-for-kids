from imutils import face_utils
from imutils import paths
import numpy as np
import argparse
import imutils
import shutil
import json
import dlib
import cv2
import sys
import os
import time


class positive_feedback(object):
    def __init__(self):
        self.sg = cv2.imread("static/img/sunglasses.png")
        self.sgMask = cv2.imread("static/img/sunglasses_mask.png")



        self.detector = cv2.dnn.readNetFromCaffe("assets/deploy.prototxt",
	               "assets/res10_300x300_ssd_iter_140000.caffemodel")

        self.predictor = dlib.shape_predictor("assets/shape_predictor_68_face_landmarks.dat")
        self.leftEyeCenter = None
        self.rightEyeCenter = None
        self.step = 10
        self.min_confidence = 0.6
        self.W = 300
        self.H = 300

        
    def detect_eyes(self,image):

        (H, W) = image.shape[:2]
        self.W = W
        self.H = H
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))

        self.detector.setInput(blob)
        detections = self.detector.forward()

        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        if confidence < self.min_confidence:
            print("[INFO] no reliable faces found")

            # use defalut eyes position
            box = [495.63419342,115.53211927,746.1227417, 445.26317596]
            box=np.array(box)
            (startX, startY, endX, endY) = box.astype("int")

            leftEyePts = [[640,236],
                [655, 225],
                [670, 224],
                [685, 231],
                [671, 238],
                [656, 239]]
            rightEyePts = [[527, 237],
                            [541, 230],
                            [556, 229],
                            [572 ,239],
                            [556 ,243],
                            [540, 244]]
            leftEyePts = np.array(leftEyePts)
            rightEyePts = np.array(rightEyePts)

        else:
            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])

            (startX, startY, endX, endY) = box.astype("int")

            rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
            shape = self.predictor(image, rect)
            shape = face_utils.shape_to_np(shape)

            (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
            (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

            leftEyePts = shape[lStart:lEnd]
            rightEyePts = shape[rStart:rEnd]

        self.leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
        self.rightEyeCenter = rightEyePts.mean(axis=0).astype("int")

        dY = self.rightEyeCenter[1] - self.leftEyeCenter[1]
        dX = self.rightEyeCenter[0] - self.leftEyeCenter[0]
        angle = np.degrees(np.arctan2(dY, dX)) - 180

        self.sg = imutils.rotate_bound(self.sg, angle)

        sgW = int((endX - startX) * 0.9)
        self.sg = imutils.resize(self.sg, width=sgW)

        sgMask = cv2.cvtColor(self.sgMask, cv2.COLOR_BGR2GRAY)
        sgMask = cv2.threshold(sgMask, 0, 255, cv2.THRESH_BINARY)[1]
        sgMask = imutils.rotate_bound(sgMask, angle)
        self.sgMask = imutils.resize(sgMask, width=sgW, inter=cv2.INTER_NEAREST)

        steps = np.linspace(0, self.rightEyeCenter[1], self.step,
            dtype="int")
        return steps

        

    def gif_generator(self,i,y,image):
        steps = np.linspace(0, self.rightEyeCenter[1], self.step,
            dtype="int")


        shiftX = int(self.sg.shape[1] * 0.25)
        shiftY = int(self.sg.shape[0] * 0.35)
        y = max(0, y )

        # add the sunglasses to the image
        output = self.overlay_image(image, self.sg, self.sgMask,
            (self.rightEyeCenter[0] - shiftX, y))
            
        cv2.putText(output, 'You are a good kid!', (300,600), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0,255,65), 3, 1)


        _, jpeg = cv2.imencode(".jpg", output)

        return jpeg.tobytes()

    
    def overlay_image(self,bg, fg, fgMask, coords):
        (sH, sW) = fg.shape[:2]
        (x, y) = coords

        overlay = np.zeros(bg.shape, dtype="uint8")

        overlay[y:y + sH, x:x + sW] = fg

        alpha = np.zeros(bg.shape[:2], dtype="uint8")
        alpha[y:y + sH, x:x + sW] = fgMask
        alpha = np.dstack([alpha] * 3)

        output = self.alpha_blend(overlay, bg, alpha)
    
        return output

    def alpha_blend(self,fg, bg, alpha):

        fg = fg.astype("float")
        bg = bg.astype("float")
        alpha = alpha.astype("float") / 255

        fg = cv2.multiply(alpha, fg)
        bg = cv2.multiply(1 - alpha, bg)

        output = cv2.add(fg, bg)

        return output.astype("uint8")
