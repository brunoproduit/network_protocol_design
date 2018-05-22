import hashlib
import re
import os
import sys
import readline
import rlcompleter
import atexit
import codecs

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

class UserInterface:
    def __init__(self):
        self.pgpsettings = {}
        if DEVELOPMENT:
            self.neighbors = {'4db526c3294f17820fd0682d9dceaeb4': 2130706433, b'aaaaaaaaaaaaaaaa': 2130706433, b'dddddddddddddddd': 2130706433 }
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
            self.enter_neighbors() # filehandling
        self.display_seperator()

        # self.routinglistener.daemon = True
        # self.messagelistener.daemon = True

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
        self.routinglistener.terminate() # HOWTO terminate a thread using python?
        self.messagelistener.terminate() # HOWTO terminate a thread using python?
        self.routinglistener.quit = True # file that tells if its readable
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

    # aufsplitten und wirklich im nachhinein ausführen, würde sicher viel bringen :)
    def recognize_command(self, input):
        # input = input.lower() # not here!

        commandparts = input.split(' ', 1)
        if len(commandparts) > 1:
            detailcommadparts = commandparts[0].split(DETAIL_SEPERATOR) # ":"
            address = commandparts[0].lower()
            message = commandparts[1]

            if len(detailcommadparts) == 2:
                address = detailcommadparts[0].lower()

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

    # sends a file based on it's filename to the given destination address
    # @param: destination_address md5 value
    # @param: filename string
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

        if(destination_address == BROADCAST_ADDRESS):
            print('handling broadcast')
        else:
            # address = self.md5_to_ip(destination_address) # nexthop
            # ip_address = router.get_next_hop(destination_address)
            ip_address = router.get_next_hop(b'dddddddddddddddd') # TODO: nothing coming back
            print(ip_address)
            if(ip_address is None):
                s.connect(('127.0.0.1', PORT))
            else:
                s.connect((adip_addressdress, PORT)) # replace 127.0.0.1 with whatever the routing translation gives you!

            if type == L5_MESSAGE:
                message = bytes(Layer3(
                    Layer4(Layer5(encrypt(raw_data, pk).encode()), L4_DATA, True, True, 1, 2, 3),
                    b'aaaaaaaaaaaaaaaa',
                    b'dddddddddddddddd',
                    # bytes.fromhex(source_address),
                    # bytes.fromhex(destination_address),
                    # codecs.decode(source_address, 'hex_codec'),
                    # codecs.decode(destination_address, 'hex_codec'),
                    7,
                    packet_type=L3_DATA))
            elif type == L5_FILE:
                message = bytes(Layer3(
                    Layer4(Layer5(encrypt_file(raw_data, pk).encode(), L5_FILE), L4_DATA, True, True, 1, 2, 3),
                    b'aaaaaaaaaaaaaaaa', # bytes.fromhex(source_address),
                    b'dddddddddddddddd', # bytes.fromhex(destination_address),
                    7,
                    packet_type=L3_DATA))

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

utils = Utils()
ui = UserInterface()
# can we actually read a new file instead of this?
source_address = Utils.address_to_md5("max@mustermann.ee") # TODO: I need some way to get the mail from a pgp file! (crypto part!)

ui.enable_history()
ui.startup()
router = Router(source_address, ui.neighbors)
ui.main_loop()
