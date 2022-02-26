# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import contextlib
import queue
import os.path
import select
import sys
import termios
import threading
import tty
from datetime import datetime
from time import time
from pycoral.utils.dataset import read_label_file
from aiymakerkit import vision


@contextlib.contextmanager
def nonblocking(f):
    def get_char():
        if select.select([f], [], [], 0) == ([f], [], []):
            return sys.stdin.read(1)
        return None

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(f.fileno())
        yield get_char
    finally:
        termios.tcsetattr(f, termios.TCSADRAIN, old_settings)


@contextlib.contextmanager
def worker(process):
    requests = queue.Queue()

    def run():
        while True:
            request = requests.get()
            if request is None:
                break
            process(request)
            requests.task_done()

    def submit(request):
        requests.put(request)

    thread = threading.Thread(target=run)
    thread.start()
    try:
        yield submit
    finally:
        requests.put(None)
        thread.join()


def save_frame(request):
    filename, frame = request
    vision.save_frame(filename, frame)
    print('Saved: %s' % filename)


def print_help(labels):
    print("Press buttons '0' .. '9' to save images from the camera.")
    if labels:
        for key in sorted(labels):
            print(key, '-', labels[key])


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--labels', '-l', type=str, default=None,
                        help='Labels file')
    parser.add_argument('--continuous', '-c', type=int, default=0,
                        help='Continuously capture the number of specified images')
    parser.add_argument('--captures_dir', '-d', type=str, default='captures',
                        help='Directory for image captures')
    parser.add_argument('--capture_device_index', '-i', type=int, default=0,
                        help='Hardware capture device index')
    args = parser.parse_args()

    labels = {}
    if args.labels:
        labels = read_label_file(args.labels)
    print_help(labels)

    with nonblocking(sys.stdin) as get_char, worker(save_frame) as submit:
        def generate_filename(label_id):
            class_dir = labels.get(label_id, str(label_id))
            timestamp = datetime.now()
            filename = "PI_CAM_" + timestamp.strftime(
                "%Y%m%d_%H%M%S%f") + '.png'
            return os.path.join(args.captures_dir, class_dir, filename)

        # Handle key events from GUI window.
        def handle_key(key, frame):
            if key == ord('q') or key == ord('Q'):
                return False  # Stop processing frames.
            if key == ord('h') or key == ord('H'):
                print_help(labels)
                return True
            if args.continuous:
                return True
            if ord('0') <= key <= ord('9'):
                label_id = key - ord('0')
                filename = generate_filename(label_id)
                submit((filename, frame.copy()))
            return True  # Keep processing frames.

        START_DELAY_SECS = 3
        SNAP_DELAY_SECS = 1 / 3
        snap_time = int()
        snap_count = int()
        continuous_active = False

        for frame, key in vision.get_frames(handle_key=handle_key,
                                            capture_device_index=args.capture_device_index,
                                            return_key=True):
            # Handle continous capture mode
            if args.continuous:
                if key is not None and (ord('0') <= key <= ord('9')):
                    label_id = key - ord('0')
                    continuous_active = True
                    start_time = time()
                if continuous_active:
                    countdown = START_DELAY_SECS - int(time() - start_time)
                    # Snap the specified number of pics
                    if snap_count < args.continuous:
                        if countdown > 0:
                            vision.draw_label(frame,
                                              'GET READY IN: ' + str(countdown))
                            print('Get ready in: ', countdown, end='\r')
                        else:
                            # Wait a little between frames
                            if time() - snap_time > SNAP_DELAY_SECS:
                                filename = generate_filename(label_id)
                                submit((filename, frame.copy()))
                                snap_time = time()
                                snap_count += 1
                    elif time() - snap_time > 1:  # Artificial delay to let the last save finish
                        label_name = str(label_id)
                        label_name += ' (' + labels[
                            label_id] + ')' if labels else ''
                        print('Captured', snap_count,
                              'photos for label ' + label_name)
                        snap_count = 0
                        continuous_active = False
            # Handle key events from console.
            ch = get_char()
            if ch is not None and not handle_key(ord(ch), frame):
                break


if __name__ == '__main__':
    main()
