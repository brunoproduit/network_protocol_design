import hashlib
import re
import os
import sys
import readline
import rlcompleter
import atexit
from utils import *
from constants import *
from settings import *
from routingprocesses import *
from constants import *
from routing import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *

#TODO: ACK Packet / Packet Factory
#TODO: find out how to get the nexthop from routing :)

class UserInterface:
    def __init__(self):
        self.pgpsettings = {}
        if DEVELOPMENT:
            self.neighbors = {'4db526c3294f17820fd0682d9dceaeb4': 2130706433}
        else:
            self.neighbors = {}
        self.routinglistener = RoutingListener('0.0.0.0', ROUTER_PORT)
        self.messagelistener = RoutingListener('0.0.0.0', PORT)

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
            self.enter_neighbors()
        self.display_seperator()

        self.routinglistener.start() # router is listening now
        self.messagelistener.start() # also messages will be displayed now!

    # main loop routine with command recognition an respond
    def main_loop(self):
        commandType = 'empty'
        while commandType != QUIT_COMMAND:
            commandInput = input('')
            commandType = self.recognize_command(commandInput)
            if commandType == HELP_COMMAND:
                self.display_help()
        self.routinglistener.join()
        self.routinglistener.quit = True
        print("cya next time!!")

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

    def recognize_command(self, input):
        input = input.lower()

        commandparts = input.split(' ', 1)
        if len(commandparts) > 1:
            detailcommadparts = commandparts[0].split(DETAIL_SEPERATOR) # ":"
            address = commandparts[0]
            message = commandparts[1]

            if len(detailcommadparts) == 2:
                address = detailcommadparts[0]

                if not utils.valid_destination(address):
                    print("Address seems to be invalid, doublecheck your input after the @-sign")
                    return HELP_COMMAND
                if detailcommadparts[1] == SEND_FILE_COMMAND:
                    self.send_file(address, message)
                    return SEND_FILE_COMMAND
                if detailcommadparts[1] == SEND_MESSAGE_COMMAND:
                    self.send_message(address, message)
                    return SEND_MESSAGE_COMMAND
                else:
                    print("Unkonwn command detail, doublecheck your input after the :-sign")
                    return INVALID_COMMAND
            else:
                if not utils.valid_destination(address):
                    print("Address seems to be invalid, please doublecheck your input after the @-sign")
                    return INVALID_COMMAND
                self.send_message(address, message)
                return SEND_MESSAGE_COMMAND
        elif input == QUIT_COMMAND:
            return QUIT_COMMAND
        else:
            return HELP_COMMAND

    def send_file(self, destination_address, file_name):
        file_data = Utils.read_file(file_name)
        if not file_data:
            print("File: ", file_name, ", doesn't exist, not sending anything")
        else:
            self.send_message(destination_address, file_data, L5_FILE)

    # sends a message through a new udp socket
    # @param: destination_address string (mail)
    # @param: raw_data string, payload
    # @param: type string, type of message defaults to L5_MESSAGE
    def send_message(self, destination_address, raw_data, type = L5_MESSAGE):
        destination_address = Utils.address_to_md5(destination_address)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('127.0.0.1', PORT)) # replace 127.0.0.1 with whatever the routing translation gives you!

        message = bytes(Layer3(
            Layer4Data(Layer5(encrypt(raw_data, pk).encode()), True, True, 1, 2, 3),
            b'aaaaaaaaaaaaaaaa', # bytes.fromhex(source_address),
            b'dddddddddddddddd', # bytes.fromhex(destination_address),
            7,
            packet_type=type))

        print(message)

        try:
            s.sendall(message)
        except Exception as e:
            print (e, 'Terminating server ...')

    def forward_packet(self, l5packet, nexthop):
        print("Fowarding Layer 5 packet")

    def display_help(self):
        print(HELP_TEXT)

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

    # def listen_to_neighbors(self):
    #     self.routinglistener.start()
    #     print ("Listening for routing data on port: " + str(port))

    def send_to_neighbors(self):
        for neighbor in self.neighbors:
            # print(self.neighbors[neighbor])
            # print(neighbor)
            self.sender_neighbor(str(ipaddress.IPv4Address(self.neighbors[neighbor])))

    #not actually needed as a new process!
    def sender_neighbor(self, address):
        sender = RoutingSender(address, ROUTER_PORT)
        sender.start()
        sender.join()

utils = Utils()
ui = UserInterface()
sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.ee")
source_address = Utils.address_to_md5("max@mustermann.ee") # TODO: I need some way to get the mail from a pgp file! (crypto part!)

ui.enable_history()
ui.startup()
ui.main_loop()
