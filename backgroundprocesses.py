import select
import socket
import threading

from globals import unconfirmed_message_queue
from command import Command
from constants import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *
from messageFactory import MessageFactory


class BackgroundListener(threading.Thread):

    def __init__(self, address, port, sk):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port
        self.sk = sk  # should be global as well I guess!

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        s.bind((self.address, self.port))


        # Receive loop
        while True:
            ready = select.select([s], [], [], 1)
            if ready[0]:
                data, addr = s.recvfrom(1024)
                l3_data = Layer3.parse_l3(data)

                # sending ACKs
                if l3_data.type != L3_CONFIRMATION:
                    ack = MessageFactory.createACK(l3_data.destination, l3_data.source, l3_data.packet_number)
                    # disable next line to test acks
                    Command.execute(SEND_MESSAGE_COMMAND, ack)  # confirm incoming message immediately

                if(l3_data.payload != b''):
                    l4_data = l3_data.payload
                    l5_data = l3_data.payload.payload

                # receiving ACKs
                if l3_data.type == L3_CONFIRMATION:
                    # not working because it's a new process and no thread.

                    global unconfirmed_message_queue
                    del unconfirmed_message_queue[l3_data.confirmation_id]
                    Utils.print_new_chat_line('LOG: Confirmation of the message: ' + str(l3_data.confirmation_id))
                elif l5_data.type.encode() == L5_MESSAGE:
                    data = decrypt(l5_data.payload, self.sk)
                    Utils.print_new_chat_line(l3_data.source + ' : ' + data)
                elif l5_data.type.encode() == L5_FILE:
                    data = decrypt(l5_data.payload, self.sk)
                    Utils.print_new_chat_line(l3_data.source + ' : ' + data)
                    Utils.write_file('download.tmp', '.', data.encode())
                    # data = decrypt_file('download.tmp', self.sk)  # not working appearently
                    # file_name = l3_data.source.split('\x00', 1)[0]
                    # file_data = l3_data.source.split('\x00', 1)[1]
                    # file_data = l3_data
                    # print(l3_data.source, ': sent you a file;', file_name)
                    # Utils.write_file(file_name, '.', file_data.encode())
                else:
                    # print('\n', l3_data.source + "$: sent you something I can't handle\n chat$ ")
                    # print(l3_data.source, ':', data)
                    Utils.print_new_chat_line(l3_data.source + "$: sent you something I can't handle")