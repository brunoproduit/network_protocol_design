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

class UserInterface:
    def __init__(self):
        self.pgpsettings = {}
        if DEVELOPMENT:
            self.neighbors = {'4db526c3294f17820fd0682d9dceaeb4': 2130706433}
        else:
            self.neighbors = {}
        self.routinglistener = RoutingListener('0.0.0.0', ROUTER_PORT)

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

        self.listen_to_neighbors()
        self.send_to_neighbors()
    
    # Message other than routing should also be done with processes, 
    # as we could receive messages anytime - Bruno
    def main_loop(self):
        commandType = 'empty'
        while commandType != QUIT_COMMAND:
            commandInput = input('Give me a command: ')
            commandType = self.recognize_command(commandInput) # command pattern should probably be used instead of this rubish implementation :D
            # print(commandType)
            if commandType == HELP_COMMAND:
                self.display_help()
        self.routinglistener.join()
        # Cannot do this after join, and wouldn't work either way, the loop should be done here
        # and call the process - Bruno 
        self.routinglistener.quit = True
        print("cya next time!!")


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
                    print("Address seems to be invalid, please doublecheck your input after the @-sign")
                    return HELP_COMMAND
                if detailcommadparts[1] == SEND_FILE_COMMAND:
                    self.send_file(address, message)
                    return SEND_FILE_COMMAND
                if detailcommadparts[1] == SEND_MESSAGE_COMMAND:
                    self.send_message(address, message)
                    return SEND_MESSAGE_COMMAND
                else:
                    print("Unkonwn command detail, please doublecheck your input after the :-sign")
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

    def send_file(self, address, filename):
        address = utils.address_to_md5(address)
        filedata = utils.read_file(filename)
        if not filedata:
            print ("File: " + filename + ", doesn't exist, not sending anything")
        else:
            print("Preparing packet for file #X, sending out to address: " + address + ", filecontent is: " + str(filedata))

    def send_message(self, address, message):
        address = utils.address_to_md5(address)
        print("Preparing packet for message #X, sending out to address: " + address + ", message is: " + message)
        
        # Where is our pk? - Bruno
        ciphertext = encrypt(message, pk).encode()
        
        # You need to tell me what you did with routing
        # We need router.py - Bruno
        ip = get_next_hop(address)
        
        # When do we chunk? is this giving us already l3 chunks or
        # should we chunk in this method? - Bruno
        chunks = bytes(Layer3(ciphertext))
        
        # Sending
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ip, PORT))      
        
        for i in chunks:
            s.sendall(i)
            

    def forward_packet(self, l5packet):
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

            self.neighbors[utils.address_to_md5(mail)] = int(ipaddress.IPv4Address(ip))
            # backwards conversion: str(ipaddress.IPv4Address(3232235521))
            addmore = input('Add more neighbors? y/n ')
        print("Neighbors given:", self.neighbors)

    def listen_to_neighbors(self):
        self.routinglistener.start()
        print ("Listening for routing data on port: " + str(ROUTER_PORT))

    def send_to_neighbors(self):
        for neighbor in self.neighbors:
            # print(self.neighbors[neighbor])
            # print(neighbor)
            self.sender_neighbor(str(ipaddress.IPv4Address(self.neighbors[neighbor])))

    def sender_neighbor(self, address):
        sender = RoutingSender(address, ROUTER_PORT)
        sender.start()
        sender.join()

utils = Utils()
ui = UserInterface()
ui.enable_history()
ui.startup()
ui.main_loop()

# ui.cleanup_history_vars()
