import cv2 as cv

import consts


def is_video_ext(filename):
    return filename.lower().endswith(consts.VIDEO_FILE_EXTENSIONS)

def is_image_ext(filename):
    return filename.lower().endswith(consts.IMAGE_FILE_EXTENSIONS)

def count_frames_in_video(video_filename):
    assert is_video_ext(video_filename)

    video = cv.VideoCapture(video_filename)
    return int(video.get(cv.CAP_PROP_FRAME_COUNT))