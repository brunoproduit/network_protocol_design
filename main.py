#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Libraries
import hashlib
import re
import os
import sys
import readline
import rlcompleter
import atexit
import codecs
from argparse import ArgumentParser

# Internal imports
from utils import *
from constants import *
from backgroundprocesses import *
from constants import *
from routing import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *
from command import *
from messageFactory import *

# router = None

class UserInterface:
    def __init__(self):
        self.routinglistener = BackgroundListener('0.0.0.0', ROUTER_PORT, sk)  # TODO: Only for neighbors
        self.messagelistener = BackgroundListener('0.0.0.0', PORT, sk)

    def enable_history(self):
        # tab completion
        readline.parse_and_bind('tab: complete')
        # history file
        histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

    def cleanup_history_vars(self):
        atexit.register(readline.write_history_file, histfile)
        del os, histfile, readline, rlcompleter

    # startup routine from user interface
    def startup(self):
        print("Welcome to our uber-cool implementation of the NPD Protocol Stack")
        self.display_seperator()

        self.routinglistener.start()  # router is listening now
        self.messagelistener.start()  # also messages will be displayed now!

    # main loop routine with command recognition an respond
    def main_loop(self):
        commandType = 'empty'
        while commandType != QUIT_COMMAND:
            commandInput = input('')
            commandType, payload = self.recognize_command(commandInput)
            Command.execute(commandType, payload)
        self.routinglistener.terminate()
        self.messagelistener.terminate()
        print("cya next time!!")

    # recognizes the command and returns it's type and payload
    def recognize_command(self, input):
        commandparts = input.split(' ', 1)
        if len(commandparts) > 1:
            detailcommadparts = commandparts[0].split(DETAIL_SEPERATOR)
            destination_address = commandparts[0].lower()
            payload = commandparts[1]  # can be either Textmessage or a Filename

            if len(detailcommadparts) == 2:
                destination_address = detailcommadparts[0].lower()
                if not Utils.valid_destination(destination_address):
                    return INVALID_COMMAND, "Address seems to be invalid, doublecheck your input after the @-sign"
                if detailcommadparts[1] == SEND_FILE_COMMAND:
                    file_data = Utils.read_file(payload)
                    if not file_data:
                        return INVALID_COMMAND, "File: " + payload + ", doesn't exist, not sending anything"
                    payload = MessageFactory.createFileMessage(source_address, destination_address, file_data, pk)
                    return SEND_FILE_COMMAND, payload
                if detailcommadparts[1] == SEND_MESSAGE_COMMAND:
                    payload = MessageFactory.createTextMessage(source_address, destination_address, payload, pk)
                    return SEND_MESSAGE_COMMAND, payload
                else:
                    return INVALID_COMMAND, "Unkonwn command detail, doublecheck your input after the :-sign"
            else:
                if not Utils.valid_destination(destination_address):
                    return INVALID_COMMAND, "Address seems to be invalid, please doublecheck your input after the @-sign"
                payload = MessageFactory.createTextMessage(source_address, destination_address, payload, pk)
                return SEND_MESSAGE_COMMAND, payload
        elif input == QUIT_COMMAND:
            return QUIT_COMMAND, None
        else:
            return HELP_COMMAND, None

    def display_seperator(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# Main, Program entry, arg parsing
if __name__ == '__main__':

    parser = ArgumentParser(description='%s by %s, version %s' % (NAME, AUTHOR, VERSION))

    parser.add_argument('-m', '--masterkey', help='Master key file to use', type=str,
                        default=MASTERKEYPATH)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--createkey', help='If no key is given with --pubkey, \
                         this can be used to create a fresh key pair', type=str, default=None)
    group.add_argument('-p', '--pubkey', help='public key file to use', type=str,
                       default=SOURCEKEYPATH)

    args = parser.parse_args()

    if args.createkey:
        # can we actually read a new file instead of this?
        source_address = Utils.address_to_md5("max@mustermann.ee")
        print('Source address:', source_address)
        sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.ee")

    elif args.pubkey:
        sk = read_key_from_file(args.pubkey)
        pk = sk.pubkey

    utils = Utils()
    ui = UserInterface()
    ui.enable_history()

    ui.display_seperator()
    print('Reading in neighbors from ', NEIGHBORSFILE)
    neighbors = Utils.read_neighbors_from_neighborfile()
    print(neighbors)
    print('Finished reading neighbors')
    ui.display_seperator()

    global router
    router = Router(source_address, neighbors)

    ui.startup()
    ui.main_loop()
