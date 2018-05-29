import multiprocessing
import select
import socket

from command import Command
from constants import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *
from globals import unconfirmed_message_queue

# Thread instead of process
from messageFactory import MessageFactory


class BackgroundListener(multiprocessing.Process):

    def __init__(self, address, port, sk):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port
        self.sk = sk  # should be global as well I guess!

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        s.bind((self.address, self.port))


        # Receive loop
        while True:
            # try:
                ready = select.select([s], [], [], 1)
                if ready[0]:
                    data, addr = s.recvfrom(1024)
                    l3_data = Layer3.parse_l3(data)

                    # sending ACKs
                    if l3_data.type != L3_CONFIRMATION:
                        ack = MessageFactory.createACK(l3_data.destination, l3_data.source, l3_data.packet_number)
                        Command.execute(SEND_MESSAGE_COMMAND, ack)  # confirm incoming message immediately
                        # global unconfirmed_message_queue
                        # unconfirmed_message_queue.append(l3_data)


                    if(l3_data.payload != b''):
                        l4_data = l3_data.payload
                        l5_data = l3_data.payload.payload

                    # receiving ACKs
                    if l3_data.type == L3_CONFIRMATION:
                        # not working because it's a new process and no thread.

                        # global unconfirmed_message_queue
                        # unconfirmed_message_queue.remove(l3_data)  # TODO: maybe rather remove it by a dictionary!
                        print('Confirmation of the message: ', l3_data.packet_number)
                    elif l5_data.type.encode() == L5_MESSAGE:
                        data = decrypt(l5_data.payload, self.sk)
                        print(l3_data.source, ': ', data)
                    elif l5_data.type.encode() == L5_FILE:
                        data = decrypt(l5_data.payload, self.sk)
                        print(data)
                        Utils.write_file('download.tmp', '.', data.encode())
                        # data = decrypt_file('download.tmp', self.sk)  # not working appearently
                        # file_name = l3_data.source.split('\x00', 1)[0]
                        # file_data = l3_data.source.split('\x00', 1)[1]
                        # file_data = l3_data
                        # print(l3_data.source, ': sent you a file;', file_name)
                        # Utils.write_file(file_name, '.', file_data.encode())
                    else:
                        print(l3_data.source, ": sent you something I can't handle")
                        print(l3_data.source, ':', data)

        # except Exception:
            #     print('Something went wrong..')
        s.close()
        print ('Closed the server socket')
        print ('Terminating ...')
