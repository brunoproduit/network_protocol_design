#!/usr/bin/python3
from struct import *
from constants import *

LAYER3_FORMAT = "BHBBH10p10p"


class Layer3:
    def __init__(self, source=b'', destination=b'', packet=0, packet_type=L3_DATA, confirmation=0):
        self.version = 1
        self.packet_number = packet
        self.type = packet_type
        self.ttl = 15
        self.confirmation_id = confirmation
        self.source = source
        self.destination = destination
        # self.layer4 TODO Payload

    def serialize(self):
        return pack(LAYER3_FORMAT,
                    self.version,
                    self.packet_number,
                    self.type,
                    self.ttl,
                    self.confirmation_id,
                    self.source,
                    self.destination)

    def deserialize(self, source):
        data = unpack(LAYER3_FORMAT, source)
        self.version = data[0]
        self.packet_number = data[1]
        self.type = data[2]
        self.ttl = data[3]
        self.confirmation_id = data[4]
        self.source = data[5]
        self.destination = data[6]
