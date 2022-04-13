import os.path
import enum
import platform
import sys

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.adapters import detect
from pycoral.utils import edgetpu

_EDGETPU_SHARED_LIB = {
    'Linux': 'libedgetpu.so.1',
    'Darwin': 'libedgetpu.1.dylib',
    'Windows': 'edgetpu.dll'
}[platform.system()]

VIDEO_SIZE = (1920, 1080)
CORAL_COLOR = (86, 104, 237)
BLUE = (255, 0, 0)  # BGR (not RGB)

def get_frames(title='Camera', size=VIDEO_SIZE, handle_key=None,
               capture_device_index=0, mirror=True, return_key=False):
    """
    Gets a stream of image frames from the camera.

    Args:
      title: A title for the display window.
      size: The image resolution for all frames, as a tuple (x, y).
      handle_key: A callback function that accepts arguments (key, frame) for a key event and
        the image frame from the moment the key was pressed.
      capture_device_index: The Linux device ID for the camera.
      mirror: Whether to flip the image horizontally (set True for a selfie view).
      return_key: Whether to also return any key presses. If True, the function returns a tuple with
        (frame, key) instead of just the frame.

    Returns:
      An iterator that yields each image frame from the default camera. Or a tuple if ``return_key``
      is True.
    """
    width, height = size

    if not handle_key:
        print("Press Q to quit")

        def handle_key(key, frame):
            if key == ord('q') or key == ord('Q'):
                return False
            return True

    attempts = 5
    while True:
        cap = cv2.VideoCapture(capture_device_index)
        success, _ = cap.read()
        if success:
            print("Camera started successfully.")
            break

        if attempts == 0:
            print(
                "Cannot initialize camera!\nMake sure the camera is connected.",
                file=sys.stderr)
            sys.exit(1)

        cap.release()
        attempts -= 1

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    try:
        while True:
            key = cv2.waitKey(1)
            success, frame = cap.read()
            if mirror:
                frame = cv2.flip(frame, 1)
            if success:
                if return_key:
                    yield (frame, key)
                else:
                    yield frame
                cv2.imshow(title, frame)

            if key != -1 and not handle_key(key, frame):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def save_frame(filename, frame):
    """
    Saves an image to a specified location.

    Args:
      filename: The path where you'd like to save the image.
      frame: The bitmap image to save.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    cv2.imwrite(filename, frame)
