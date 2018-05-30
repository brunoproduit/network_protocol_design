#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Libraries
import readline
from argparse import ArgumentParser

from messageFactory import *
from backgroundprocesses import *


class UserInterface:
    def __init__(self):
        self.routinglistener = BackgroundListener('0.0.0.0', ROUTER_PORT, sk)
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

    # startup routine from user interface
    def startup(self):
        print("Welcome to our uber-cool implementation of the NPD Protocol Stack")
        self.display_seperator()

        self.routinglistener.start()  # router is listening now
        self.messagelistener.start()  # also messages will be displayed now!

        # do the routing startup / start the routing update routine for every 30 seconds!

    # main loop routine with command recognition an respond
    def main_loop(self):
        commandType = 'empty'
        while commandType != QUIT_COMMAND:
            commandInput = input('chat$ ')
            commandType, payload = self.recognize_command(commandInput)
            Command.execute(commandType, payload)

        self.routinglistener.terminate()
        self.messagelistener.terminate()
        print("cya next time!!")

    # recognizes the command and returns it's type and payload
    def recognize_command(self, input):
        commandparts = input.split(' ', 1)

        if input.startswith(MD5_COMMAND + ' '):
            return MD5_COMMAND, input[4:]

        if len(commandparts) > 1:
            # handle address based commands
            detail_command_parts = commandparts[0].split(DETAIL_SEPERATOR)
            destination_address = commandparts[0].lower()
            payload = commandparts[1]  # can be either text-message or a filename

            if len(detail_command_parts) == 2:
                destination_address = detail_command_parts[0].lower()

                if not Utils.valid_destination(destination_address):
                    return INVALID_COMMAND, "Address seems to be invalid, double-check your input after the @-sign"

                if detail_command_parts[1] == SEND_FILE_COMMAND:
                    file_data = Utils.read_file(payload)
                    if not file_data:
                        return INVALID_COMMAND, "File: " + payload + ", doesn't exist, not sending anything"

                    payload = MessageFactory.createFileMessage(source_address, destination_address, payload, file_data, pk)
                    return SEND_FILE_COMMAND, payload

                if detail_command_parts[1] == SEND_MESSAGE_COMMAND:
                    payload = MessageFactory.createTextMessage(source_address, destination_address, payload, pk)
                    return SEND_MESSAGE_COMMAND, payload

                else:
                    return INVALID_COMMAND, "Unknown command detail, double-check your input after the :-sign"

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
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")


# Main, Program entry, arg parsing
if __name__ == '__main__':

    parser = ArgumentParser(description='%s by %s, version %s' % (NAME, AUTHOR, VERSION))

    parser.add_argument('-c', '--createkey', help='This can be used to create a fresh key pair',\
            nargs='?', default="create")
    
    args = parser.parse_args()

    if args.createkey!="create":
        source_address = Utils.address_to_md5("max@mustermann.ee")
        print('Source address:', source_address)
        sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.ee")

    
    utils = Utils()
    ui = UserInterface()
    ui.enable_history()
    ui.startup()
    ui.main_loop()
