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
from settings import *
from backgroundprocesses import *
from constants import *
from routing import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *
from command import *
from messageFactory import *

class UserInterface:
    def __init__(self):
        self.pgpsettings = {}
        if DEVELOPMENT:
            self.neighbors = {'4db526c3294f17820fd0682d9dceaeb4': 2130706433, b'aaaaaaaaaaaaaaaa': 2130706433, b'dddddddddddddddd': 2130706433 }
        else:
            self.neighbors = {}
        self.routinglistener = BackgroundListener('0.0.0.0', ROUTER_PORT, sk)
        self.messagelistener = BackgroundListener('0.0.0.0', PORT, sk)


    # parses the pgp settings file
    # @return: true on parsing false if the file doesn't exist/needs to be overwritten
    def read_pgpkey_settings_file(self):
        if not os.path.exists(SETTINGSFILE) or input("Do you want to overwrite existing settings? (y/n) ").lower() == "y":
            return False
        else:
            print("Reading from settings file...")
            with open(SETTINGSFILE, 'rb') as f:
               for line in f:
                   settings = line[:-1].decode('utf8').split('=', 1)
                   self.add_pgpkey(settings[1], settings[0])
            print("Reading settings finished...")
            return True

    def input_and_add_pgpkey(self, keyname):
        filename = input("Insert path for the " + keyname + ": ")
        self.add_pgpkey(filename, keyname)

    def add_pgpkey(self, filename, keyname):
        if not os.path.exists(filename):
            print (keyname + ": '" + filename + "', can't work without provided key.")
            sys.exit(1)
        else:
            keyfile = open(filename, 'rb')
            self.pgpsettings[keyname] = PGPSetting(os.path.abspath(keyfile.name), keyfile.read())
            print("Adding '" + keyname + "' with value '" + os.path.abspath(keyfile.name) + "'")
            keyfile.close()

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

        if not self.read_pgpkey_settings_file():
            self.input_and_add_pgpkey(MASTER_KEY_NAME)
            self.input_and_add_pgpkey(SELF_KEY_NAME)
            utils.save_settings(self.pgpsettings)

        self.display_seperator()
        if not DEVELOPMENT:
            self.enter_neighbors() # filehandling
        self.display_seperator()

        self.routinglistener.start() # router is listening now
        self.messagelistener.start() # also messages will be displayed now!


    # main loop routine with command recognition an respond
    def main_loop(self):
        commandType = 'empty'
        while commandType != QUIT_COMMAND:
            commandInput = input('')
            commandType, payload = self.recognize_command(commandInput)
            Command.execute(commandType, payload)
        self.routinglistener.terminate() # HOWTO terminate a thread using python?
        self.messagelistener.terminate() # HOWTO terminate a thread using python?
        self.routinglistener.quit = True # file that tells if its readable
        print("cya next time!!")

    # recognizes the command and returns it's type and payload
    def recognize_command(self, input):
        commandparts = input.split(' ', 1)
        if len(commandparts) > 1:
            detailcommadparts = commandparts[0].split(DETAIL_SEPERATOR) # ":"
            destination_address = commandparts[0].lower()
            payload = commandparts[1] # can be either Textmessage or a Filename

            if len(detailcommadparts) == 2:
                destination_address = detailcommadparts[0].lower()
                if not utils.valid_destination(destination_address):
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
                if not utils.valid_destination(destination_address):
                    return INVALID_COMMAND, "Address seems to be invalid, please doublecheck your input after the @-sign"
                payload = MessageFactory.createTextMessage(source_address, destination_address, payload, pk)
                return SEND_MESSAGE_COMMAND, payload
        elif input == QUIT_COMMAND:
            return QUIT_COMMAND, None
        else:
            return HELP_COMMAND, None

    def forward_packet(self, l5packet, nexthop):
        print("Fowarding Layer 5 packet")

    def display_seperator(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # neighbors could also be saved in the settings file..
    def enter_neighbors(self):
        print("Add your neighbors:")
        addmore = 'y'
        while addmore.lower() == 'y':
            ip = 'invalid'
            while not utils.valid_ip(ip):
                ip = input('IP: ')

            mail = 'invalid'
            while not utils.valid_mail(mail):
                mail = input('mail: ')

            self.neighbors[Utils.address_to_md5(mail)] = int(ipaddress.IPv4Address(ip))
            # backwards conversion: str(ipaddress.IPv4Address(3232235521))
            addmore = input('Add more neighbors? y/n ')
        print("Neighbors given:", self.neighbors)

    def send_to_neighbors(self):
        for neighbor in self.neighbors:
            self.sender_neighbor(self.md5_to_ip(neighbor))

    def md5_to_ip(self, md5):
        if md5 in self.neighbors:
            return str(ipaddress.IPv4Address(self.neighbors[md5]))
        else:
            return None

    def sender_neighbor(self, address):
        # send all the routing data! :D
        sender = RoutingSender(address, ROUTER_PORT)
        sender.start()
        sender.join()

# Main, Program entry, arg parsing
if __name__ == '__main__':

    parser = ArgumentParser(description='%s by %s, version %s' % (NAME, AUTHOR, VERSION))
    parser.add_argument('-c', '--createkey', help='If no key is given with --pubkey, \
                         this can be used to create a fresh key pair', type=str, default=None)
    parser.add_argument('-p', '--pubkey', help='public key file to use', type=str,
                        default=SOURCEKEYPATH)
    args = parser.parse_args()
    
    if args.createkey:
    # can we actually read a new file instead of this?
        source_address = Utils.address_to_md5("max@mustermann.ee") # TODO: I need some way to get the mail from a pgp file! (crypto part!)
        sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.ee")
    
    else:
        sk = read_key_from_file(args.pubkey)
        pk = sk.pubkey
        
    utils = Utils()
    ui = UserInterface()

    ui.enable_history()
    ui.startup()
    # router = Router(source_address, ui.neighbors)
    ui.main_loop()
