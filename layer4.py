#!/usr/bin/python3
from constants import L4_DATA, L4_CHUNKED, L4_ENCRYPTED, L4_ROUTINGFULL
from layer5 import Layer5
from routing_table import RoutingTable
from utils import Utils


class Layer4:
    def __init__(self, data, packet_type, encrypted=True, chunked=True, status=0, stream_id=0, chunk_id=0):
        self.type = packet_type

        if encrypted and packet_type != L4_ROUTINGFULL:
            self.type = self.type ^ L4_ENCRYPTED

        if chunked and packet_type != L4_ROUTINGFULL:
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
                Utils.int_to_bytestring(self.chunk_id, 8)
            ).encode() + bytes(self.payload)
        elif self.type & L4_ROUTINGFULL:
            return chr(self.type).encode() + bytes(self.payload)
        else:
            raise ValueError('Layer 4 unsupported packet!')

    @staticmethod
    def parse_l4(packet):
        if packet[0] & L4_DATA:
            return Layer4(
                packet_type=L4_DATA,
                data=Layer5.parse_l5(packet[13:]),
                encrypted=packet[0] & L4_ENCRYPTED,
                chunked=packet[0] & L4_CHUNKED,
                status=packet[1],
                stream_id=int.from_bytes(packet[2:5], byteorder='big'),
                chunk_id=int.from_bytes(packet[5:13], byteorder='big'),
            )
        elif packet[0] & L4_ROUTINGFULL:
            return Layer4(
                packet_type=L4_ROUTINGFULL,
                data=RoutingTable.parse(packet[1:])
            )
