#  Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
#  All rights reserved.
#  A copy of the license can be found at the LICENSE file, or the link https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE



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