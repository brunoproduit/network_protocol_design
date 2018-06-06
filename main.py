#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Libraries
import os
import readline
from argparse import ArgumentParser


from backgroundprocesses import *
from packetEngine import StreamManager
from utils import *

class UserInterface:
    def __init__(self):
        self.routinglistener = BackgroundListener('0.0.0.0', ROUTER_PORT, sk)
        self.messagelistener = BackgroundListener('0.0.0.0', PORT, sk)
        self.stream_mgr = StreamManager(pk)

    def __del__(self):
        print("cya next time!!")

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

        self.routinglistener.setDaemon(True)  # router is listening now
        self.messagelistener.setDaemon(True)  # also messages will be displayed now!
        self.routinglistener.start()  # router is listening now
        self.messagelistener.start()  # also messages will be displayed now!

        # do the routing startup / start the routing update routine for every 30 seconds!

    # main loop routine with command recognition an respond
    def main_loop(self):
        is_quit = 0
        while is_quit != 1:
            command_input = input('')
            is_quit = self.execute_command(command_input)

    # recognizes the command and returns it's type and payload
    def execute_command(self, input):
        commandparts = input.split(' ', 1)

        if input.startswith(MD5_COMMAND + ' '):
            print(input[4:], ':', Utils.address_to_md5(input[4:]))
            return 0

        if len(commandparts) > 1:
            # handle address based commands
            detail_command_parts = commandparts[0].split(DETAIL_SEPERATOR)
            destination_address = commandparts[0].lower()
            payload = commandparts[1]  # can be either text-message or a filename

            if len(detail_command_parts) == 2:
                destination_address = detail_command_parts[0].lower()

                if not Utils.valid_destination(destination_address):
                    print("Address seems to be invalid, double-check your input after the @-sign")
                    return 0
                if detail_command_parts[1] == SEND_FILE_COMMAND:
                    file_data = Utils.read_file(payload)
                    if not file_data:
                        print("File: " + payload + ", doesn't exist, not sending anything")
                        return 0

                    self.stream_mgr.add_stream(source_address, destination_address, file_data, True, payload)
                    return 0
                if detail_command_parts[1] == SEND_MESSAGE_COMMAND:
                    self.stream_mgr.add_stream(source_address, destination_address, payload)
                    return 0
                else:
                    print("Unknown command detail, double-check your input after the :-sign")
                    return 0
            else:
                if not Utils.valid_destination(destination_address):
                    print("Address seems to be invalid, please doublecheck your input after the @-sign")
                    return 0

                self.stream_mgr.add_stream(source_address, destination_address, payload)
                return 0

        elif input == QUIT_COMMAND:
            print ('Exiting...')
            return 1
        else:
            print(HELP_TEXT)
            return 0

    def display_seperator(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")


# Main, Program entry, arg parsing
if __name__ == '__main__':

    parser = ArgumentParser(description='%s by %s, version %s' % (NAME, AUTHOR, VERSION))

    parser.add_argument('-c', '--createkey', help='This can be used to create a fresh key pair',
        nargs='?', default="create")
    parser.add_argument('-n', '--name', help='Set the name of the key pair to be created',
                        nargs='?', default="name")

    args = parser.parse_args()

    if args.createkey != "create" and args.name != "name":
        source_address = args.createkey
        print('Source address:', source_address)
        sk, pk = create_pgpkey(args.name, source_address)
        write_key_to_file(sk, pk, MASTERPREFIX)

    elif (args.createkey != "create") != (args.name != "name"):
        print('Both name and create need to be set in order to create a new key pair!')
        exit(1)

    else:
        print('Reading keys from ', MASTERPREFIX, '[priv|pub]key.pem, if this fails use the --createkey options to start!')
        sk = read_key_from_file(MASTERPREFIX + 'privkey.pem')
        pk = read_key_from_file(MASTERPREFIX + 'pubkey.pem')
        print('done reading keys..')


    utils = Utils()
    ui = UserInterface()
    ui.enable_history()
    ui.startup()
    ui.main_loop()
    del(ui)
