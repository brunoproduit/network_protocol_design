#!/usr/bin/python3
# -*- coding: utf-8 -*-

# General -----------------------------------------------------------------------------------------------------------
NAME = 'Network protocol design chat '                                                        # Name of program
AUTHOR = 'Sander Mikelsaar, Sasan Reyaeifars, Florian Reiter, Bruno Produit, Pavel Chikul'    # Author of program
VERSION = '0.1'                                                                               # Version of program
DEVELOPMENT = True

# UDP -----------------------------------------------------------------------------
PORT = 1337                             # Default UDP port, can be changed in arg
INET_ADDR = '127.0.0.1'                 # Default IP, can be changed in arg
UDP_RECEIVE_BUFFER_SIZE = 1024*1024     # Maximum buffer for receiving
MAX_PDU_SIZE = 100                      # Maximum PDU for communication

#Protocol -------------------------------------------------------------------------
ROUTER_PORT = 9999
TEST_MD5_SRC = 'a'*20
BROADCAST_ADDRESS = '0' * 32

# Utils ---------------------------------------------------------------------------
SETTINGSFILE = 'settings.ini'
MASTERKEYPATH = './keys/masterkey.pgp'
SOURCEKEYPATH = './keys/sourcekey.pgp'
MASTER_KEY_NAME = 'master_key'
SELF_KEY_NAME = 'own_node_key'
ALLKEYSPATH = ''

# Commands ------------------------------------------------------------------------
BROADCAST_MAIL = "@all"
DETAIL_SEPERATOR = ":"
SEND_FILE_COMMAND = "file"
SEND_MESSAGE_COMMAND = "message"
QUIT_COMMAND = "quit"
HELP_COMMAND = "help"
HELP_TEXT = "The following commands are valid:\n @mail[:file] - Message with spaces. (e.g. @maxmu@ttu.ee:file secret.doc, @mimmu@ttu.ee Hello World!)\n @all[:file] - Message with spaces to everyone. (e.g. @all:file secret.doc, @all Hello World!)\n help - Display help. \n quit - Exit the program"
UNKNOWN_COMMAND = "unknown"
INVALID_COMMAND = "invalid"

# L5 ------------------------------------------------------------------------
L5_MESSAGE = b'\x01'
L5_FILE = b'\x02'
L5_HASH = b'\x04'

# L4 ------------------------------------------------------------------------
L4_ROUTINGFULL = 1
L4_DATA = 2
L4_CHUNKED = 4
L4_ENCRYPTED = 8

# L3 ------------------------------------------------------------------------
L3_DATA = 0x02
L3_CONFIRMATION = 0x04
