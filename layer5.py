#!/usr/bin/python3
from constants import L5_MESSAGE


class Layer5:
    # Constructor
    # @param: data bytes
    # @param: packet_type Layer5Type, defaults to MESSAGE
    def __init__(self, data, packet_type=L5_MESSAGE):
        self.type = packet_type
        self.payload = data
    
    # Serializing the packet to be called as bytes(l5p)
    # @return: packet bytes
    def __bytes__(self):
        return chr(self.type).encode() + self.payload
    
    # Parses a serialized l5 packet
    # @static
    # @param: packet string
    # @return: l5p Layer5
    @staticmethod
    def parse_l5(packet):
        return Layer5(packet[1:], packet[0])
