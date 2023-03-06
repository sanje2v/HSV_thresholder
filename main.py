import os
import argparse
import cv2 as cv
import pyperclip as clipboard

from utils import *


WINDOW_SOURCE_MEDIA_NAME = 'Source'
WINDOW_DETECTION_NAME = 'Thresholding'
FRAME_IDX_NAME = 'Frame index'
LOW_H_NAME = 'Low Hue'
LOW_S_NAME = 'Low Saturation'
LOW_V_NAME = 'Low Value'
HIGH_H_NAME = 'High Hue'
HIGH_S_NAME = 'High Saturation'
HIGH_V_NAME = 'High Value'
MAX_VALUE = 255
MAX_VALUE_H = 360 // 2

low_H = 0
low_S = 0
low_V = 0
high_H = MAX_VALUE_H
high_S = MAX_VALUE
high_V = MAX_VALUE
video_src = None
frame_idx = -1
playing = True


def on_frame_idx_changed(val):
    global input_file, video_src, frame_idx, playing

    if not playing and video_src is not None:
        video_src.release()
        video_src = cv.VideoCapture(input_file)
        for _ in range(val):
            video_src.grab()
        frame_idx = val
        ret, frame = video_src.read()
        if ret:
            frame_HSV = rescale_convert_and_show(frame, args.scale, WINDOW_SOURCE_MEDIA_NAME)
            frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
            cv.imshow(WINDOW_DETECTION_NAME, frame_threshold)

def on_low_H_thresh_changed(val):
    global low_H
    global high_H
    low_H = min(high_H-1, val)
    cv.setTrackbarPos(LOW_H_NAME, WINDOW_DETECTION_NAME, low_H)

def on_high_H_thresh_changed(val):
    global low_H
    global high_H
    high_H = max(val, low_H+1)
    cv.setTrackbarPos(HIGH_H_NAME, WINDOW_DETECTION_NAME, high_H)

def on_low_S_thresh_changed(val):
    global low_S
    global high_S
    low_S = min(high_S-1, val)
    cv.setTrackbarPos(LOW_S_NAME, WINDOW_DETECTION_NAME, low_S)

def on_high_S_thresh_changed(val):
    global low_S
    global high_S
    high_S = max(val, low_S+1)
    cv.setTrackbarPos(HIGH_S_NAME, WINDOW_DETECTION_NAME, high_S)

def on_low_V_thresh_changed(val):
    global low_V
    global high_V
    low_V = min(high_V-1, val)
    cv.setTrackbarPos(LOW_V_NAME, WINDOW_DETECTION_NAME, low_V)

def on_high_V_thresh_changed(val):
    global low_V
    global high_V
    high_V = max(val, low_V+1)
    cv.setTrackbarPos(HIGH_V_NAME, WINDOW_DETECTION_NAME, high_V)

def on_window_clicked(event, x, y, flags, param):
    global playing

    if event == cv.EVENT_LBUTTONDOWN:
        # Play/Pause
        playing = not playing

    elif event == cv.EVENT_MBUTTONDOWN:
        # Copy to clipboard
        print("Copying to clipboard...")
        clipboard.copy(f"({low_H}, {low_S}, {low_V}), ({high_H}, {high_S}, {high_V})")


parser = argparse.ArgumentParser()
parser.add_argument('input_filename', type=str, default='', help='Image or video filename')
parser.add_argument('--scale', type=float, default=1.0, help='Scale image before displaying')
args = parser.parse_args()

input_file = args.input_filename
if not input_file or not os.path.isfile(input_file) or not (is_image_ext(input_file) or is_video_ext(input_file)):
    print("Please pass an existing video or image file!")
    exit(-1)

print("Left click to start/stop video playback and middle mouse click to copy HSV range to clipboard.")
print("Press 'q' or 'Esc' to quit.")

cv.namedWindow(WINDOW_SOURCE_MEDIA_NAME)
cv.namedWindow(WINDOW_DETECTION_NAME)

cv.setMouseCallback(WINDOW_SOURCE_MEDIA_NAME, on_window_clicked, {'winname': WINDOW_SOURCE_MEDIA_NAME})
cv.setMouseCallback(WINDOW_DETECTION_NAME, on_window_clicked, {'winname': WINDOW_DETECTION_NAME})

if is_video_ext(input_file):
    total_frames = count_frames_in_video(input_file)
    cv.createTrackbar(FRAME_IDX_NAME, WINDOW_DETECTION_NAME, 0, total_frames-1, on_frame_idx_changed)
cv.createTrackbar(LOW_H_NAME, WINDOW_DETECTION_NAME , low_H, MAX_VALUE_H, on_low_H_thresh_changed)
cv.createTrackbar(HIGH_H_NAME, WINDOW_DETECTION_NAME , high_H, MAX_VALUE_H, on_high_H_thresh_changed)
cv.createTrackbar(LOW_S_NAME, WINDOW_DETECTION_NAME , low_S, MAX_VALUE, on_low_S_thresh_changed)
cv.createTrackbar(HIGH_S_NAME, WINDOW_DETECTION_NAME , high_S, MAX_VALUE, on_high_S_thresh_changed)
cv.createTrackbar(LOW_V_NAME, WINDOW_DETECTION_NAME , low_V, MAX_VALUE, on_low_V_thresh_changed)
cv.createTrackbar(HIGH_V_NAME, WINDOW_DETECTION_NAME , high_V, MAX_VALUE, on_high_V_thresh_changed)

def rescale_convert_and_show(frame, scale, winname):
    if args.scale != 1.0:
        frame = cv.resize(frame, None, fx=scale, fy=scale)
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    cv.imshow(winname, frame)
    return frame_HSV

if is_image_ext(input_file):
    frame = cv.imread(input_file)
    frame_HSV = rescale_convert_and_show(frame, args.scale, WINDOW_SOURCE_MEDIA_NAME)

while True:
    if is_video_ext(input_file) and playing:
        if frame_idx == -1:
            video_src = cv.VideoCapture(input_file)
        ret, frame = video_src.read()
        if not ret:
            frame_idx = -1
            continue
        frame_HSV = rescale_convert_and_show(frame, args.scale, WINDOW_SOURCE_MEDIA_NAME)
        frame_idx += 1
        cv.setTrackbarPos(FRAME_IDX_NAME, WINDOW_DETECTION_NAME, frame_idx)

    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    cv.imshow(WINDOW_DETECTION_NAME, frame_threshold)
    key = cv.waitKey(1)
    if key in [ord('q'), ord('Q'), 27]:
        break

video_src.release()
cv.destroyAllWindows()