from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *
from utils import *


class MessageFactory:
    @staticmethod
    def createTextMessage(source_address, destination_address, raw_data, pk):
        destination_address = Utils.address_to_md5(destination_address)

        return Layer3(
            Layer4(
                Layer5(
                    encrypt(raw_data, pk).encode(),
                    L5_MESSAGE),
                L4_DATA, True, True, 1, 2, 3),
            bytes.fromhex(source_address),
            bytes.fromhex(destination_address),
            7,
            packet_type=L3_DATA)


    # sends a file based on it's filename to the given destination address
    # @param: destination_address md5 value
    # @param: filename string
    @staticmethod
    def createFileMessage(source_address, destination_address, filename, raw_data, pk):
        destination_address = Utils.address_to_md5(destination_address)
        return Layer3(
            Layer4(Layer5(encrypt_file(filename + '\00' + raw_data, pk).encode(), L5_FILE), L4_DATA, True, True, 1, 2, 3),
            # b'aaaaaaaaaaaaaaaa',
            # b'dddddddddddddddd',
            bytes.fromhex(source_address),
            bytes.fromhex(destination_address),
            7,
            packet_type=L3_DATA)

    # forms a basic ACK message out of src, dest and pk
    @staticmethod
    def createACK(source_address, destination_address, pk):
        return Layer3(
            Layer4(
                Layer5(
                    encrypt(None, pk),
                    0),

            )
        )

    # creates a routingtable-connect message
    # @param: source_address md5 value
    # @param: destination_address md5 value
    # @param: routingtable bytes from RoutingTable.__bytes__()
    # @param: pk public key of the recipient
    @staticmethod
    def createConnectMessage(source_address, destination_address, routingtable, pk):
        destination_address = Utils.address_to_md5(destination_address)
        return Layer3(
            Layer4(Layer5(encrypt(routingtable, pk).encode()), L4_ROUTINGFULL, True, True, 1, 2, 3),
            bytes.fromhex(source_address),
            bytes.fromhex(destination_address))

    # creates a routingtable-disconnect message
    # @param: destination_address md5 value
    # @param: routingtable bytes from RoutingTable.__bytes__()
    # @param: pk public key of the recipient
    @staticmethod
    def createDisconnectMessage(source_address, destination_address, pk):
        destination_address = Utils.address_to_md5(destination_address)
        return Layer3(
            Layer4(Layer5(encrypt(None, pk)), L4_ROUTINGFULL),
            bytes.fromhex(source_address),
            bytes.fromhex(destination_address))
