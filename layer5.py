#!/usr/bin/python3
from enum import Enum

class Layer5Type(Enum):
    MESSAGE = b'\x01',
    FILE = b'\x02',
    HASH = b'\x04'

class Layer5:

    # Constructor
    # @param: data
    # @param: packet_type Layer5Type, defaults to MESSAGE
    def __init__(self, data, packet_type=Layer5Type.MESSAGE):
        self.type = packet_type
        self.payload = data
    
    # Serializing the packet to be called as bytes(l5p)
    # @return: packet bytes
    def __bytes__(self):
        return self.type.value[0] + self.payload
    
# Parses a serialized l5 packet
# @param: packet Layer5
# @return: l5p Layer5
def parse_l5(packet):
    return Layer5(packet[1:], packet[0])
        

        
