import multiprocessing
import select
import socket
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *

sk, pk = create_pgpkey("Max Mustermann", "max@mustermann.ee")

class RoutingListener(multiprocessing.Process):

    def __init__(self, address, port):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port
        self.quit = False

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        s.bind((self.address, self.port))


        # Receive loop
        while not self.quit: # quit appearently doesn't work / maybe bruno knows :)
            # try:
                ready = select.select([s], [], [], 1)
                if ready[0]:
                    data, addr = s.recvfrom(1024)
                    print('You just received a message from: ', addr)
                    l3_data = Layer3.parse_l3(data)
                    l5_data = l3_data.payload.payload
                    data = decrypt(l5_data.payload, sk)
                    # print(l5_data.type)

                    if l5_data.type.encode() == L5_MESSAGE:
                        print(l3_data.source, ': ', data)
                    elif l5_data.type.encode() == L5_FILE:
                        file_name = l3_data.source.split('\x00', 1)[0]
                        file_data = l3_data.source.split('\x00', 1)[1]
                        print(l3_data.source, ': sent you a file;', file_name)
                        Utils.write_file(file_name, '.', file_data)
                    elif l5_data.type.encode() == L5_HASH:
                        print(l3_data.source, ': sent you a hash;') #
                    else:
                        print(l3_data.source, ": sent you something I can't handle")
                        print(l3_data.source, ':', data)


            # except Exception as e:
                # print (e, 'Terminating server ...')
                # break

        s.close()
        print ('Closed the server socket')
        print ('Terminating ...')

class RoutingSender(multiprocessing.Process):

    def __init__(self, ip_source_address, port, data, source_address, destination_address):
        multiprocessing.Process.__init__(self)
        self.address = ip_source_address
        self.port = port


    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('127.0.0.1', PORT)) # replace 127.0.0.1 with whatever the routing translation gives you!

        print(self.source_address)
        print(bytes.fromhex(self.source_address))

        message = bytes(Layer3(
            Layer4Data(Layer5(encrypt(raw_data, pk).encode()), True, True, 1, 2, 3),
            bytes.fromhex(source_address),
            bytes.fromhex(destination_address),
            7,
            packet_type=L3_DATA))

        print(message)

        try:
            s.sendall(message)
        except Exception as e:
            print (e, 'Terminating server ...')
