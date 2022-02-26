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
from pycoral.utils.dataset import read_label_file
from aiymakerkit import vision
import models

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-m', '--model', default=models.CLASSIFICATION_MODEL,
                    help='File path of .tflite file. Default is vision.CLASSIFICATION_MODEL')
parser.add_argument('-l', '--labels', default=models.CLASSIFICATION_LABELS,
                    help='File path of labels file. Default is vision.CLASSIFICATION_LABELS')
args = parser.parse_args()

classifier = vision.Classifier(args.model)
labels = read_label_file(args.labels)

for frame in vision.get_frames():
    classes = classifier.get_classes(frame, top_k=1, threshold=0.3)
    if classes:
        score = classes[0].score
        label = labels.get(classes[0].id)
        vision.draw_label(frame, f'{label}: {round(score, 4)}')
