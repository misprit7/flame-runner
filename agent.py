#!/usr/bin/env python

from controls.pad import Button, Pad, Stick, Trigger
import cv2, pathlib, os, time

dump_url = pathlib.Path('rtsp://localhost:8554/dolphin')

# while len(os.listdir(dump_dir)) == 0: time.sleep(0.001)

time.sleep(0.5)

vidcap = cv2.VideoCapture(str(dump_url))
# last_frame_num = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)-1
# vidcap.set(cv2.CAP_PROP_POS_FRAMES, last_frame_num-10)

while True:
    ret, image = vidcap.read()
    # last_frame_num = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)-1
    if not ret:
        print('read failed!')
        break

    cv2.imshow('image',image)
    # cv2.waitKey(0)
    # time.sleep(1/60)
    time.sleep(0.001)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # time.sleep(0.0001)

