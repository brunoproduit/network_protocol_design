#!/usr/bin/python3
from struct import *
from layer5 import *


class Layer4:
    # Constructor
    # @param: data bytes
    # @param encrypted boolean
    # @param chunked boolean
    # @param: packet_type Layer4Type, defaults to DATA
    def __init__(self, data, encrypted, chunked, packet_type=L4_DATA):
        self.type = packet_type
        
        if encrypted:
            self.type = self.type ^ L4_ENCRYPTED
        
        if chunked:
            self.type = self.type ^ L4_CHUNKED
            
        self.payload = data
    
    # Serializing the packet to be called as bytes(l4p)
    # @return: packet bytes
    def __bytes__(self):
        return (chr(self.type) + str(bytes(self.payload))).encode()
    
    # Parses a serialized l4 packet
    # @static
    # @param: packet string
    # @return: l5p Layer4
    @staticmethod
    def parse_l4(packet):
        if packet[0] & L4_DATA:
            return Layer4Data.parse_l4data(packet)
        elif packet[0] & L4_ROUTINGFULL:
            raise ValueError('Layer 4 Routing packet not supported!')
        else:
            raise ValueError('Layer 4 packet of unknown type!')

class Layer4Data:
    def __init__(self, data, encrypted, chunked, status, stream_id, chunk_id):
        self.type = L4_DATA
        
        if encrypted:
            self.type = self.type ^ L4_ENCRYPTED
        
        if chunked:
            self.type = self.type ^ L4_CHUNKED
        
        self.status = status
        self.stream_id = stream_id
        self.chunk_id = chunk_id
        self.payload = data
    
    def __bytes__(self):
        return (
            chr(self.type) + 
            chr(self.status) + 
            str(bytes([self.stream_id])[0:3]) + 
            str(bytes([self.chunk_id])[0:8]) + 
            str(bytes(self.payload))).encode()
    
    @staticmethod
    def parse_l4data(packet):
        return Layer4Data(
            packet[13:], 
            packet[0] & L4_ENCRYPTED, 
            packet[0] & L4_CHUNKED, 
            packet[1],     # Status
            packet[2:5],   # Stream ID
            packet[5:13],  # Chunk ID
            )


class Layer4Routing:
    def __init__(self):
        print("Not implemented!")
