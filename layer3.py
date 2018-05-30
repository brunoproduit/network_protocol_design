#!/usr/bin/python3
from constants import L3_DATA, L3_CONFIRMATION
from layer4 import Layer4
from utils import Utils


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
            (chr(self.version) +
             Utils.int_to_bytestring(self.packet_number, 2) +
             chr(self.type) +
             chr(self.ttl) +
             Utils.int_to_bytestring(self.confirmation_id, 2) +
             chr(0)).encode() +
            self.source +
            self.destination +
            self.payload.__bytes__())
        # use the md5 hash as a integer?

    @staticmethod
    def parse_l3(packet):
        if packet[3] == L3_DATA:
            return Layer3(
                packet_type=L3_DATA,
                source=packet[8:24].hex(),
                destination=packet[24:40].hex(),
                ttl=packet[4],
                packet=int.from_bytes(packet[1:3], byteorder='big'),
                data=Layer4.parse_l4(packet[40:]),
            )
        elif packet[3] == L3_CONFIRMATION:
            return Layer3(
                packet_type=L3_CONFIRMATION,
                source=packet[8:24].hex(),
                destination=packet[24:40].hex(),
                ttl=packet[4],
                confirmation=int.from_bytes(packet[5:7], byteorder='big')
            )
