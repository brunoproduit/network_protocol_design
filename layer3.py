#!/usr/bin/python3
from struct import *
from constants import *


class Layer3:
    def __init__(self):
        self.__init__("", "", 0, L3_DATA)

    def __init__(self, source, destination, packet, packet_type=L3_DATA, confirmation=0):
        self.version = 0
        self.packet_number = packet
        self.type = packet_type
        self.ttl = 15
        self.confirmation_id = confirmation
        self.destination = destination
        self.source = source
        # self.layer4 TODO Payload
