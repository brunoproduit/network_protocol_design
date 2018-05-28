import socket

from constants import *
from utils import *
from globals import router


class Command:
    @staticmethod
    def execute(type, payload):
        if(type == SEND_MESSAGE_COMMAND or type == SEND_FILE_COMMAND):
            Command.handle_send_message(payload) # TODO: I already need the actual packet here!
        elif(type == HELP_COMMAND):
            Command.display_help()
        elif(type == INVALID_COMMAND):
            print(payload)
        elif(type == QUIT_COMMAND):
            print ('Exiting..')
        elif(type == MD5_COMMAND):
            print(payload, ':', Utils.address_to_md5(payload))


    @staticmethod
    def display_help():
        print(HELP_TEXT)

    # sends a message through a new udp socket
    # @param: destination_address string (mail)
    # @param: raw_data string, payload
    # @param: type string, type of message defaults to L5_MESSAGE
    @staticmethod
    def send_message(l3_message, ip_address):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.connect((ip_address, PORT))  # replace 127.0.0.1 with whatever the routing translation gives you!
        try:
            s.sendall(bytes(l3_message))
        except Exception as e:
            print(e, 'Terminating server ...')

    @staticmethod
    def handle_send_message(l3_message):

        global router
        if l3_message.destination.hex() == BROADCAST_ADDRESS:
            for neighbor in router.neighbors:
                Command.send_message(l3_message, neighbor[1])  # [0] = md5, [1] = ip
        #         TODO: Check if we already got this broadcast!
        else:
            address_tuple = router.get_next_hop(l3_message.destination.hex())
            if address_tuple is not None:
                ip_address = address_tuple[1]
                Command.send_message(l3_message, ip_address)
            else:
                print(l3_message.destination.hex(), ', doesn\'t exist in the neighbors list, try another Mail!')
