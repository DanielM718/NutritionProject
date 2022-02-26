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

import csv
import numpy as np
import queue
import threading

import tflite_runtime.interpreter as tflite

from . import audio_recorder

def load_labels(class_map_csv):
    """Read the class name file and return a list of strings."""
    with open(class_map_csv) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return [display_name for _, _, display_name in reader]


def classify_audio(model_file, labels_file, callback,
                   audio_device_index=0, sample_rate_hz=16000,
                   negative_threshold=0.6, num_audio_frames=4096):
    """Acquire audio, preprocess, and classify."""
    if sample_rate_hz not in (16000, 48000):
        raise ValueError('Sample rate must be 16000 Hz or 48000 Hz')

    downsample_factor = {16000: 1, 48000: 3}[sample_rate_hz]

    # Most microphones support this
    # Because the model expects 16KHz audio, we downsample 3 fold
    recorder = audio_recorder.AudioRecorder( sample_rate_hz,
        downsample_factor=downsample_factor, device_index=audio_device_index)
    labels = load_labels(labels_file)

    interpreter = tflite.Interpreter(model_path=model_file)

    input_details = interpreter.get_input_details()
    waveform_input_index = input_details[0]['index']

    output_details = interpreter.get_output_details()
    scores_output_index = output_details[0]['index']
    embeddings_output_index = output_details[1]['index']
    spectrogram_output_index = output_details[2]['index']

    interpreter.resize_tensor_input(waveform_input_index,
                                    [num_audio_frames],
                                    strict=True)
    interpreter.allocate_tensors()

    with recorder:
        print("Ready for voice commands...")
        keep_listening = True
        while keep_listening:
            waveform, _, _ = recorder.get_audio(num_audio_frames)
            waveform /= 32768.0  # Convert to [-1.0, +1.0]
            waveform = np.squeeze(waveform.astype('float32'))

            interpreter.set_tensor(waveform_input_index, waveform)
            interpreter.invoke()
            scores = interpreter.get_tensor(scores_output_index)
            scores = np.mean(scores, axis=0)
            prediction = np.argmax(scores)
            keep_listening = callback(labels[prediction], scores[prediction])


class AudioClassifier:
    """Performs classifications with a speech detection model.
    Args:
      model_file: Path to a `.tflite` speech classification model (compiled for the Edge TPU).\
      labels_file: Path to the corresponding labels file for the model.
      audio_device_index: Specify the device card for your mic. Defaults to 0.
        You can check from the command line with `arecord -l`. On Raspberry Pi, your mic must be via
        USB or a sound card HAT, because the Pi's headphone jack does not support mic input.
    """

    def __init__(self, model_file, labels_file, audio_device_index=0):
        self._thread = threading.Thread(target=classify_audio,
                                        args=(
                                            model_file, labels_file,
                                            self._callback,
                                            audio_device_index), daemon=True)
        self._queue = queue.Queue()
        self._thread.start()

    def _callback(self, label, score):
        self._queue.put((label, score))
        return True

    def next(self, block=True):
        """
        Returns a speech classification.
        Each time you call this, it pulls from a queue of recent classifications. So even if there are
        many classifications in a short period of time, this always returns them in the order received.
        Args:
          block (boolean): Whether this function should block until the next classification arrives (if
            there are no queued classification). If False, it always returns immediately and returns
            None if the classification queue is empty.
        """
        try:
            result = self._queue.get(block)
            self._queue.task_done()
            return result
        except queue.Empty:
            return None
