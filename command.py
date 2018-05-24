import socket

from constants import *

class Command:
    @staticmethod
    def execute(type, payload):
        if(type == SEND_MESSAGE_COMMAND or type == SEND_FILE_COMMAND):
            Command.send_message(payload) # TODO: I already need the actual packet here!
        elif(type == HELP_COMMAND):
            Command.display_help()
        elif(type == INVALID_COMMAND):
            print(payload)
        elif(type == QUIT_COMMAND):
            print ('Exiting..')


    @staticmethod
    def display_help():
        print(HELP_TEXT)

    # sends a message through a new udp socket
    # @param: destination_address string (mail)
    # @param: raw_data string, payload
    # @param: type string, type of message defaults to L5_MESSAGE
    @staticmethod
    def send_message(l3_message):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # print(l3_message.destination)
        # print(l3_message.type)

        print(l3_message)
        # ip_address = '127.0.0.1' # TODO: Get me from the destination address!
        global router
        ip_address = router.get_next_hop(l3_message.destination)

        s.connect((ip_address, PORT)) # replace 127.0.0.1 with whatever the routing translation gives you!
        try:
            s.sendall(bytes(l3_message))
        except Exception as e:
            print (e, 'Terminating server ...')
