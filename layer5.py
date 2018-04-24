#!/usr/bin/python3
from enum import Enum


class Layer5Type(Enum):
    MESSAGE = 0x01,
    FILE = 0x02


class Layer5:
    def __init__(self):
        self.__init__(Layer5Type.MESSAGE)

    def __init__(self, packet_type):
        self.type = packet_type
        # self.payload = ...
