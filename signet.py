

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
# SIGNET - SIGnal over NETwork#
# 19520958  - Thanh Pham Ngoc #
# 19520262  - Pham Nguyen Viet Tan #

# Packet:
# 1. Establish connection ( for Confidental, Integrity and Authentication purpose)
# 1.1
# 2.
# Packet include 16 bytes
# To avoid cryptanalyst from using same private key, we use a random IV and xor with the payload. Then we XOR them all with private key
# |IV ( 8 bytes random)| Type of Packet (1 bytes)| ID of sent packet device (essp8266) (1bytes - 254 devices, server ID =0)|
# | response (5 bytes) | checksum ( exclude the IV, by XORed them byte-by-byte)|

import socket
import os
import const


def Dict2Bytes(dict_val):
    tmp = dict_val["type"].to_bytes(1, 'big')
    tmp += dict_val["ID"].to_bytes(1, 'big')
    tmp += dict_val["response"]
    tmp += GenChecksum(tmp)
    return tmp


def Bytes2Dict(content):
    tmp = {"type": content[0], "ID": int.from_bytes(content[1:2],'big'), "response": content[2:7]}
    return tmp

def CheckChecksum(content):
    if len(content) != 8:
        raise Exception("invalid content for check-checksum")
    if content[7] ==content[1]^content[2]^content[3]^content[4]^content[5]^content[6]^content[0]:
        return 1
    return 0


def GenChecksum(content):
    return (content[1]^content[2]^content[3]^content[4]^content[5]^content[6]^content[0]).to_bytes(1,'big')


def EncryptConn(content):
    privk = const.PRIVATE_KEY # get the private key
    tmp = os.urandom(8)  # generate 64-bit random number for IV
    # make sure the content have 8 bytes length
    print(content)
    print(len(content))
    if len(content) != 8:
        raise Exception("invalid content")
    tmp = tmp+bytes(a ^ b for a, b in zip(content, tmp))
    return bytes(a ^ b for a, b in zip(privk, tmp))


def DecryptConn(content):
    privk = const.PRIVATE_KEY
    if len(content) != 16:
        raise Exception("invalid content")
    tmp = bytes(a ^ b for a, b in zip(content, privk))
    return bytes(a ^ b for a, b in zip(tmp[0:8],tmp[8:16]))


def ssend(s, content):
    s.sendall(EncryptConn(content))
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if len(data) == 0:
            break
        print("Received:", repr(data))
    print("Connection closed.")
    s.close()

