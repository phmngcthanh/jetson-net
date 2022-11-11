
#  MIT License
#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Jetson Nano SmartGate for Wens course@UIT - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# PRED - PREDict Component #
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #

import argparse
import os
import glob
import random
import time
import cv2
import numpy as np
import darknet
import const
import time
#init the model
'''
current_path =  os.getcwd()
nconfig_file = os.path.join(current_path, const.config_path, const.config_file)
ndata_file= os.path.join(current_path, const.config_path, const.data_file)
nweights = os.path.join(current_path, const.config_path, const.weights)'''
nconfig_file =  const.config_path + const.config_file
ndata_file=  const.config_path + const.data_file
nweights =  const.config_path + const.weights


network, class_names, class_colors = darknet.load_network(
    nconfig_file,
    ndata_file,
    nweights,
    batch_size=const.batch_size
)


thresh=const.thresh
def ReadCam():
    start_time = time.time()
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        raise Exception("No frame")
# press escape to exit
    cap.release()
    cv2.destroyAllWindows()
    print("ReadCam Elapsed",time.time() - start_time )
    return frame
def image_detection():
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    image = ReadCam()
    start_time = time.time()
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    print("_____---Detect---_____", detections)
    darknet.free_image(darknet_image)
    print("Darknet Elapsed", time.time() - start_time)
    return detections

