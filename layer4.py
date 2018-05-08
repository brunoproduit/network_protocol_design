#!/usr/bin/python3
from enum import Enum
from layer5 import *

class Layer4Type(Enum):
    ROUTINGFULL = b'\x01',
    DATA = b'\x02'

class Layer4Options(Enum):
    CHUNKED = b'\x04'
    ENCRYPTED = b'\x08'

class Layer4:

    # Constructor
    # @param: data bytes
    # @param encrypted boolean
    # @param chunked boolean
    # @param: packet_type Layer4Type, defaults to DATA
    def __init__(self, data, encrypted, chunked packet_type=Layer4Type.DATA):
        self.type = packet_type
        
        if encrypted:
            self.type ^= Layer4Options.ENCRYPTED.value[0]
        
        if chunked:
            self.type ^= Layer4Options.CHUNKED.value[0]
            
        self.payload = Layer5(data)
    
    # Serializing the packet to be called as bytes(l4p)
    # @return: packet bytes
    def __bytes__(self):
        return self.type.value[0] + self.payload
    
    # Parses a serialized l4 packet
    # @static
    # @param: packet string
    # @return: l5p Layer4
    def parse_l4(packet):
        return Layer4(packet[1:], packet[0])


class Layer4Routing(Layer4):
    def __init__(self):
        print("blah")


class Layer4Data(Layer4):
    def __init__(self):
        print("blah")
