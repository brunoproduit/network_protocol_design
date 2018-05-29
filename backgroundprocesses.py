import multiprocessing
import select
import socket

from constants import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *

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

                    l4_data = l3_data.payload
                    l5_data = l3_data.payload.payload

                    # TODO: select source-keys from directory or something

                    if l5_data.type.encode() == L5_MESSAGE:
                        data = decrypt(l5_data.payload, self.sk)
                        print(l3_data.source, ': ', data)
                        MessageFactory.createACK()
                    elif l5_data.type.encode() == L5_FILE:
                        data = decrypt(l5_data.payload, self.sk)
                        print (data)
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
