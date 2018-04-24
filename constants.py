#!/usr/bin/python3
# -*- coding: utf-8 -*-

# General -----------------------------------------------------------------------------------------------------------
NAME = 'Network protocol design chat '                                                        # Name of program
AUTHOR = 'Sander Mikelsaar, Sasan Reyaeifars, Florian Reiter, Bruno Produit, Pavel Chikul'    # Author of program
VERSION = '0.1'                                                                               # Version of program

# UDP -----------------------------------------------------------------------------
PORT = 7777                             # Default UDP port, can be changed in arg
INET_ADDR = '127.0.0.1'                 # Default IP, can be changed in arg
UDP_RECEIVE_BUFFER_SIZE = 1024*1024     # Maximum buffer for receiving
MAX_PDU_SIZE = 100                      # Maximum PDU for communication

#Protocol -------------------------------------------------------------------------


# Utils ---------------------------------------------------------------------------
SETTINGSGILE = 'settings.json'
MASTERKEYPATH = './keys/masterkey.pgp'
SOURCEKEYPATH = './keys/sourcekey.pgp'
ALLKEYSPATH = ''
