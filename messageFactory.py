from utils import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *

class MessageFactory:
    def createTextMessage(source_address, destination_address, raw_data, pk):
        destination_address = Utils.address_to_md5(destination_address)
        return Layer3(
            Layer4(Layer5(encrypt(raw_data, pk).encode(), L5_MESSAGE), L4_DATA, True, True, 1, 2, 3),
            b'aaaaaaaaaaaaaaaa',
            b'dddddddddddddddd',
            # bytes.fromhex(source_address),
            # bytes.fromhex(destination_address),
            # codecs.decode(source_address, 'hex_codec'),
            # codecs.decode(destination_address, 'hex_codec'),
            7,
            packet_type=L3_DATA)


    # sends a file based on it's filename to the given destination address
    # @param: destination_address md5 value
    # @param: filename string
    def createFileMessage(source_address, destination_address, raw_data, pk):
        destination_address = Utils.address_to_md5(destination_address)
        return Layer3(
            Layer4(Layer5(encrypt_file(raw_data, pk).encode(), L5_FILE), L4_DATA, True, True, 1, 2, 3),
            b'aaaaaaaaaaaaaaaa',
            b'dddddddddddddddd',
            # bytes.fromhex(source_address),
            # bytes.fromhex(destination_address),
            7,
            packet_type=L3_DATA)
