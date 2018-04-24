#!/usr/bin/python3
from struct import *
from enum import Enum


class Layer3Type(Enum):
    DATA = 0x02,
    CONFIRMATION = 0x04


class Layer3:
    def __init__(self):
        self.__init__("", "", 0, Layer3Type.DATA)

    def __init__(self, source, destination, packet, packet_type=Layer3Type.DATA, confirmation=0):
        self.version = 0
        self.packet_number = packet
        self.type = packet_type
        self.ttl = 15
        self.confirmation_id = confirmation
        self.destination = destination
        self.source = source
        # self.layer4 TODO Payload
