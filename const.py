



#  MIT License
#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Jetson Nano SmartGate for Wens course - guided by Assoc.Prof. Le Trung Quan#
# This is Jetson-Python part. The full solutions includes Jetson-Cython, ESP8266 #
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #



#This program was divided into 3 parts: Network communications, A.I Prediction and GPIO communications
import os
##### constants #####
PRIVATE_KEY = b"1952095819520262"

PORT = 19520
if os.name == "posix":
    config_path = "./trained_models/"
elif os.name == "nt":
    config_path = "C:/Users/thanh/PycharmProjects/jetsonnet/trained_models/"
else:
    print("Unsupported OS")
    exit
config_file = "yolov7-tiny.cfg"
data_file = "obj.data"
weights = "yolov7-tiny_final.weights"
batch_size = 1
thresh=0.25