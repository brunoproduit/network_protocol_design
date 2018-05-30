import threading
import time

from utils import *
from crypto import decrypt
from globals import router, unconfirmed_message_queue

from acknowledgement_thread import ConfirmMessageThread



class Command:
    # executes a command based on type and payload
    # @param: type string
    # @param: payload whatever needs to be handled (either text or bytes)
    @staticmethod
    def execute(type, payload):
        if(type == SEND_MESSAGE_COMMAND or type == SEND_FILE_COMMAND):
            Command.handle_send_message(payload)
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

        s.connect((ip_address, PORT)) # PORT could also be used somewhere else!
        try:
            s.sendall(bytes(l3_message))
        except Exception as e:
            print(e, 'Terminating server ...')

    @staticmethod
    def handle_send_message(l3_message, skipConfirmation = False):

        if not skipConfirmation:
            Command.handle_confirmation(l3_message)

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


    @staticmethod
    def handle_confirmation(l3_message):
        # Acknowledgement of messages
        if (l3_message.type != L3_CONFIRMATION):
            global unconfirmed_message_queue
            unconfirmed_message_queue[l3_message.packet_number] = l3_message  # second param is tries

            thread = threading.Thread(target=Command.confirm_message_run, args=(l3_message,))
            thread.daemon = True  # Daemonize thread
            thread.start()


    @staticmethod
    def confirm_message_run(l3_message):
        i = 0
        acked = False
        while i <= 15:
            time.sleep(2)  # 2 seconds

            if l3_message.packet_number in unconfirmed_message_queue:
                print('LOG: Resending Message', l3_message.payload.payload.payload, ',', i, 'times already tried')
                # Command.execute(SEND_MESSAGE_COMMAND, l3_message)
                Command.handle_send_message(l3_message, True)
            else:
                acked = True
                break
            i += 1
        if not acked:
            print('LOG: Neighbor', l3_message.destination,
                  'not responding - you might consider removing the neighbor from list!')
