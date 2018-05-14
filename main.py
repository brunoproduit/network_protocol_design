#!/usr/bin/python3
# -*- coding: utf-8 -*-

from constants import *
#from utils import *
from routing import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *

import socket
import sys, os
from argparse import ArgumentParser
import multiprocessing
import logging


def info(): return '%s by %s, version %s' % (NAME, AUTHOR, VERSION)


# utils = Utils()
sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.ee")


class Listener(multiprocessing.Process):

    def __init__(self, address, port):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.bind((self.address, self.port))

        # Receive loop
        while True:
            try:
                data, addr = s.recvfrom(1024)
                print('Connected by', addr)
                data = Layer3.parse_l3(data).payload.payload.payload
                data = decrypt(data, sk)
                print (data)


            except Exception as e:
                print (e, 'Terminating server ...')
                break

        s.close()
        print ('Closed the server socket')
        print ('Terminating ...')


class Sender(multiprocessing.Process):

    def __init__(self, address, port):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.address, self.port))

        while True:
            data = "Eat some rotten shtrudel!"
            message = bytes(Layer3(
                Layer4Data(Layer5(encrypt(data, pk).encode()), True, True, 1, 2, 3),
                bytes.fromhex("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
                bytes.fromhex("dddddddddddddddddddddddddddddddd"),
                7,
                packet_type=L3_DATA))

            try:
                s.sendall(message)
            except Exception as e:
                print (e, 'Terminating server ...')
                break


class RouterProcess(multiprocessing.Process):
    def __init__(self, port, neighbors):
        multiprocessing.Process.__init__(self)
        self.port = port
        self.neighbors = neighbors

    def run(self):
        router = Router(TEST_MD5_SRC, self.neighbors)


# Main, Program entry, arg parsing
if __name__ == '__main__':
    parser = ArgumentParser(description=info())
    parser.add_argument('-H', '--host', help='Server TCP port, '
                        'defaults to %s' % INET_ADDR,
                        default=INET_ADDR)
    parser.add_argument('-p', '--port', type=int, help='Server TCP port, '
                        'defaults to %d' % PORT, default=PORT)

    args = parser.parse_args()

    # router = RouterProcess(ROUTER_PORT, neighbors)
    # router.start()
    # router.join()

    listener = Listener('0.0.0.0', PORT)
    sender = Sender(args.host, PORT)

    listener.start()
    sender.start()

    listener.join()
    sender.join()
