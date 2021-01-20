#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

from flask import Flask, render_template, Response
from motion_detection import SingleMotionDetector
from imutils.video import VideoStream
import threading
import datetime
import imutils
import time
import cv2

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

def detect_motion(frameCount):
  global vs, outputFrame, lock

  md = SingleMotionDetector(accumWeight=0.1)
  total = 0

  while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = imutils.rotate(frame, angle=180)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7),0)

    timestamp = datetime.datetime.now()
    cv2.putText(frame, timestamp.strftime(
        "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    if total > frameCount:
      motion = md.detect(gray)
      if motion is not None:
        (thresh, (minX, minY, maxX, maxY)) = motion
        cv2.rectangle(frame, (minX, minY), (maxX, maxY),
            (0, 0, 255), 2)

    md.update(gray)
    total += 1

    with lock:
      outputFrame = frame.copy()

def generate():
  global outputFrame, lock
  while True:
    with lock:
      if outputFrame is None:
        continue

      (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
      if not flag:
        continue

    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
        bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
  return Response(generate(),
    mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
  t = threading.Thread(target=detect_motion, args=(32,))
  t.daemon = True
  t.start()

  app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)

vs.stop()
