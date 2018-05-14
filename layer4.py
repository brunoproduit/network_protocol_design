#!/usr/bin/python3
from constants import *
from layer5 import Layer5
from utils import Utils


class Layer4:
    def __init__(self, data, packet_type, encrypted=True, chunked=True, status=0, stream_id=0, chunk_id=0):
        self.type = packet_type
        
        if encrypted:
            self.type = self.type ^ L4_ENCRYPTED
        
        if chunked:
            self.type = self.type ^ L4_CHUNKED
        
        self.status = status
        self.stream_id = stream_id
        self.chunk_id = chunk_id
        self.payload = data
    
    def __bytes__(self):
        if self.type & L4_DATA:
            return (
                chr(self.type) + 
                chr(self.status) + 
                Utils.int_to_bytestring(self.stream_id, 3) + 
                Utils.int_to_bytestring(self.chunk_id, 8) + 
                (self.payload.__bytes__()).decode()
            ).encode()
        elif self.type & L4_ROUTINGFULL:
            return (
                chr(self.type) + 
                (self.payload.__bytes__()).decode()
            ).encode()
        else:
            raise ValueError('Layer 4 unsupported packet!')
    
    @staticmethod
    def parse_l4(packet):
        if packet[0] & L4_DATA:
            return Layer4(
                data=Layer5.parse_l5((packet[13:]).decode()), 
                packet_type=L4_DATA,
                encrypted=packet[0] & L4_ENCRYPTED, 
                chunked=packet[0] & L4_CHUNKED, 
                status=packet[1],
                stream_id=Utils.bytes_to_int(packet[2:5]),
                chunk_id=Utils.bytes_to_int(packet[5:13]),
            )
        elif packet[0] & L4_ROUTINGFULL:
            raise ValueError('Layer 4 Routing packet not supported!')

