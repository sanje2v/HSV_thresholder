# HSV Thresholder
Python and OpenCV based HSV color space thresholder that works on both images and videos.

This project uses source code from OpenCV tutorials and is distributed under GPL v3 license.

## Getting Started
### Install
Install Python packages as follows:

`pip install requirements.txt`

Please refer to documentation for `pyperclip` if copying to clipboard is not working.

### Usage
You can pass an image or video via command line as follows:

`python main.py ./test.mp4 --scale=0.5`

The `scale` parameter is optional and can be used when the frame size of the image is too big to work on.


### Control
#### For videos
* When a video is playing, left click on the image area to start/pause playback.
* It is only possible to seek to a frame index when the video is paused.

#### For both images and videos
* Use mouse middle button to copy the HSV parameters as `(low hue, low saturation, low value), (high hue, high saturation, high value)` to system clipboard.
* Press `q` or `Escape` key to quit.

### Screenshot
![Usage](demo/HSVThresholder_usage.gif)

## License
GPL v3