#!/usr/bin/python3
# -*- coding: utf-8 -*-

from constants import *
import socket
import sys, os
from argparse import ArgumentParser
import multiprocessing
import logging

def info(): return '%s by %s, version %s' % (NAME, AUTHOR, VERSION)

class Listener(multiprocessing.Process):

    def __init__(self, address, port):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port
    
    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((INET_ADDR, self.port))
           
        # Receive loop
        while True:
            try: 
                data, addr = s.recvfrom(1024)
                print('Connected by', addr)
                print (data)
               
            except :
                print ('Terminating server ...')
                break
                
        s.close()
        print ('Closed the server socket')
        print ('Terminating ...')

class Sender(multiprocessing.Process):

    def __init__(self, address, port):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.address = address
        self.port = port
        
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.address, self.port))
        
        while True:
            message = b'hello world'

            try:
                s.sendall(message)
            except :
                print ('Terminating server ...')
                break

# Main, Program entry, arg parsing    
if __name__ == '__main__':
    parser = ArgumentParser(description=info())
    parser.add_argument('-H','--host', help='Server TCP port, '\
                        'defaults to %s' % INET_ADDR, \
                        default=INET_ADDR)
    parser.add_argument('-p','--port', type=int, help='Server TCP port, '\
                        'defaults to %d' % PORT, default=PORT)
    
    args = parser.parse_args()

    listener = Listener(INET_ADDR, PORT)
    sender = Sender(INET_ADDR, PORT)
    
    listener.start()
    sender.start()
    
    listener.join()
    sender.join()
    
