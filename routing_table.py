#!/usr/bin/python3


class RoutingTable:
    def __init__(self, table={}):
        self.table = table

    def __bytes__(self):
        result = bytes(0)
        for key, value in self.table.items():
            result = result + key + bytes([value]) 
        return result

    @staticmethod
    def parse(data):
        if len(data) % 17 != 0:
            raise ValueError('Incorrect size of routing table! (' + str(len(data)) + ')')

        result = RoutingTable()
        i = 0
        while i < len(data):
            result.table[data[i : i+16]] = data[i+16]
            i += 17
        return result
        