

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

#sudo pip install Jetson.GPIO


#This program was divided into 3 parts: Network communications, A.I Prediction and GPIO communications

##### Network communications#####
# We relied on Wifi encryption, instead of using our self made encryption#
import const
import datetime

import socket
import traceback


import signet
import pred
import time
serverSocket = socket.socket()

# Bind the tcp socket to an IP and port

serverSocket.bind(("0.0.0.0", 19520))
# Keep listening
serverSocket.listen()

try:
    while (True):
        # Keep accepting connections from clients

        (clientConnection, clientAddress) = serverSocket.accept()
        recvdata=clientConnection.recv(1024)[0:1]
        if recvdata ==b"1":
            start_time = time.time()
            clientConnection.send(pred.DotheMagic())
            clientConnection.send(b'\n')
            print("Response Elapsed", time.time() - start_time)

        '''
        recvdata=clientConnection.recv(1024)[0:16]
        print(len(recvdata))
        print(type(recvdata))
        tmp = signet.DecryptConn(recvdata)
        print((recvdata, tmp))
        a=b"19520958"
        tmp = signet.EncryptConn(a)
        clientConnection.send(tmp+b"\n")
        # Send current server time to the client
    
        serverTimeNow = "%s" % datetime.datetime.now()
    
        clientConnection.send(serverTimeNow.encode())
        '''
        clientConnection.close();
except:
    traceback.print_exc()
    serverSocket.close();