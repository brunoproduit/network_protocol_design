#!/usr/bin/python3
# -*- coding: utf-8 -*-

from routing import *

# General -----------------------------------------------------------------------------------------------------------
NAME = 'Network protocol design chat '                                                        # Name of program
AUTHOR = 'Sander Mikelsaar, Sasan Reyaeifars, Florian Reiter, Bruno Produit, Pavel Chikul'    # Author of program
VERSION = '1.0'                                                                               # Version of program
DEVELOPMENT = True
DEBUG = False

# UDP -----------------------------------------------------------------------------
PORT = 1338                             # Default UDP port, can be changed in arg
INET_ADDR = '127.0.0.1'                 # Default IP, can be changed in arg
UDP_RECEIVE_BUFFER_SIZE = 1024*1024     # Maximum buffer for receiving
MAX_PDU_SIZE = 100                      # Maximum PDU for communication
ACK_TIMEOUT = 5                        # ACK timewait waiting in seconds
SEND_RETRIES = 1                        # Times to retry if send is unsuccessful

#Protocol -------------------------------------------------------------------------
ROUTER_PORT = 8999
TEST_MD5_SRC = 'a'*20
BROADCAST_ADDRESS = '0' * 32

# Utils ---------------------------------------------------------------------------
NEIGHBORSFILE = 'neighbors.ini'
# MASTERKEYPATH = './keys/masterkey.pgp'
# SOURCEKEYPATH = './keys/sourcekey.pgp'
MASTERPREFIX = './keys/master'
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
HELP_TEXT = "The following commands are valid:\n @mail[:file] - Message with spaces. (e.g.\
@maxmu@ttu.ee:file secret.doc, @mimmu@ttu.ee Hello World!)\n @all[:file] - Message with spaces to\
everyone. (e.g. @all:file secret.doc, @all Hello World!)\n md5 text to convert to md5 \n help -\
Display help. \n quit - Exit the program\n"
UNKNOWN_COMMAND = "unknown"
INVALID_COMMAND = "invalid"
MD5_COMMAND = "md5"

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

# Message Status ------------------------------------------------------------
MSG_NOTREADY = 1
MSG_READY = 2
MSG_TIMEOUT = 4

# Globals -------------------------------------------------------------------
source_address = 'f'*32
