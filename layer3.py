#!/usr/bin/python3
from constants import *
from layer4 import *
from utils import *


class Layer3:
    def __init__(self, data=b'', source=b'', destination=b'', packet=0, ttl=15, packet_type=L3_DATA, confirmation=0):
        self.version = 1
        self.packet_number = packet
        self.type = packet_type
        self.ttl = ttl
        self.confirmation_id = confirmation
        self.source = source
        self.destination = destination
        self.payload = data

    def __bytes__(self):
        return (
            chr(self.version) +
            Utils.int_to_bytestring(self.packet_number, 2) +
            chr(self.type) +
            chr(self.ttl) +
            Utils.int_to_bytestring(self.confirmation_id, 2) +
            chr(0) +
            self.source.encode() +
            self.destination.encode() +
            (self.payload.__bytes__()).decode()).encode()

    @staticmethod
    def parse_l3(packet):
        if packet[3] == L3_DATA:
            return Layer3(
                Layer4Data.parse_l4data(packet[40:]),
                Utils.bytes_to_int(packet[8:24]),  # Source
                Utils.bytes_to_int(packet[24:40]), # Destination
                Utils.bytes_to_int(packet[1:2]),   # Packet number
                packet[4],
                L3_DATA,
                Utils.bytes_to_int(packet[5:6]),   # Confirmation ID
                )
        elif packet[3] == L3_CONFIRMATION:
            raise ValueError('Layer 3 ACK packet not supported!')
