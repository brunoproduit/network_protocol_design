#!/usr/bin/python3
from enum import Enum
from layer5 import *

class Layer4Type(Enum):
    ROUTINGFULL = 1,
    DATA = 2,
    CHUNKED = 4,
    ENCRYPTED = 8

class Layer4:

    # Constructor
    # @param: data bytes
    # @param encrypted boolean
    # @param chunked boolean
    # @param: packet_type Layer4Type, defaults to DATA
    def __init__(self, data, encrypted, chunked, packet_type=Layer4Type.DATA.value[0]):
        self.type = packet_type
        
        if encrypted:
            self.type = self.type ^ Layer4Type.ENCRYPTED.value
        
        if chunked:
            self.type = self.type ^ Layer4Type.CHUNKED.value
            
        self.payload = Layer5(data)
    
    # Serializing the packet to be called as bytes(l4p)
    # @return: packet bytes
    def __bytes__(self):
        return (chr(self.type) + str(bytes(self.payload))).encode()
    
    # Parses a serialized l4 packet
    # @static
    # @param: packet string
    # @return: l5p Layer4
    def parse_l4(packet):
        return Layer4(packet[1:], True, False, packet[0])


class Layer4Routing(Layer4):
    def __init__(self):
        print("blah")


class Layer4Data(Layer4):
    def __init__(self):
        print("blah")
