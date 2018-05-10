import hashlib
import re
import os
import sys
from utils import *
from constants import *
from settings import *

class UserInterface:
    def __init__(self):
        self.pgpsettings = {}

    def startupRoutine(self):
        print("Welcome to our uber-cool implementation of the NPD Protocol Stack")
        # check if a settings.json is present otherwise read masterfile and own key

        if not self.readPGPKeySettings():
            self.enterPGPKey(MASTER_KEY_NAME)
            self.enterPGPKey(SELF_KEY_NAME)
            Utils().saveSettings(self.pgpsettings)

    def readPGPKeySettings(self):
        if not os.path.exists(SETTINGSFILE) or input("Do you want to overwrite existing settings? (y/n) ").lower() == "y":
            return False
        else:
            print("Reading from settings file...")
            with open(SETTINGSFILE, 'rb') as f:
               for line in f:
                   kvpair = line[:-1].decode('utf8').split('=', 1)
                   self.addPGPKeyToSettings(kvpair[1], kvpair[0])
            return True


    def enterPGPKey(self, keyname):
        filename = input("Insert path for the " + keyname + ": ")
        self.addPGPKeyToSettings(filename, keyname)

    def addPGPKeyToSettings(self, filename, keyname):
        if not os.path.exists(filename):
            print (keyname + ": '" + filename + "', can't work without provided key.")
            sys.exit(1)
        else:
            keyfile = open(filename, 'rb')
            self.pgpsettings[keyname] = PGPSetting(os.path.abspath(keyfile.name), keyfile.read())
            print("Adding '" + keyname + "' with value '" + os.path.abspath(keyfile.name) + "'")
            keyfile.close()

    def mainLoop(self):
        commandType = 'empty'
        while commandType != QUIT_COMMAND:
            commandInput = input('Give me a command: ')
            commandType = self.commandRecogination(commandInput) # command pattern should probably be used instead of this rubish implementation :D
            print(commandType)
            if commandType == HELP_COMMAND:
                self.displayHelp()
        print("cya next time!!")


    def commandRecogination(self, input):
        input = input.lower()

        commandparts = input.split(' ', 1)
        if len(commandparts) > 1:
            detailcommadparts = commandparts[0].split(DETAIL_SEPERATOR) # ":"
            address = commandparts[0]
            message = commandparts[1]

            if len(detailcommadparts) == 2:
                address = detailcommadparts[0]

                if not self.checkAddressValid(address):
                    print("Address seems to be invalid, please doublecheck your input after the @-sign")
                    return HELP_COMMAND
                if detailcommadparts[1] == SEND_FILE_COMMAND:
                    self.sendFile(address, message)
                    return SEND_FILE_COMMAND
                if detailcommadparts[1] == SEND_MESSAGE_COMMAND:
                    self.sendMessage(address, message)
                    return SEND_MESSAGE_COMMAND
                else:
                    return HELP_COMMAND
            else:
                print (self.checkAddressValid(address))
                if not self.checkAddressValid(address):
                    print("Address seems to be invalid, please doublecheck your input after the @-sign")
                    return HELP_COMMAND
                self.sendMessage(address, message)
                return SEND_MESSAGE_COMMAND
        elif input == QUIT_COMMAND:
            return QUIT_COMMAND
        else:
            return HELP_COMMAND

    def sendFile(self, address, filename):
        address = self.addressToMD5(address)
        filedata = Utils().readFile(filename)
        if not filedata:
            print ("File: " + filename + ", doesn't exist, not sending anything")
        else:
            print("Preparing packet for file #X, sending out to address: " + address + ", filecontent is: " + str(filedata))

    def sendMessage(self, address, message):
        address = self.addressToMD5(address)
        print("Preparing packet for message #X, sending out to address: " + address + ", message is: " + message)

    def displayHelp(self):
        print(HELP_TEXT)

    def checkAddressValid(self, address):
        return re.match(r"[^@]+@[^@]+\.[^@]+", address[1:]) or address == BROADCAST_MAIL or re.match(r"[^@]+@[^@]+\.[^@]+", address) or address == BROADCAST_MAIL[1:]

    def addressToMD5(self, address):
        if address != BROADCAST_MAIL:
            m = hashlib.md5()
            m.update(str.encode(address))
            return m.hexdigest()
        else:
            return 32 * '0'


ui = UserInterface()
ui.startupRoutine()
ui.mainLoop()
