import multiprocessing
import select
import socket
from crypto import *
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
            try:
                ready = select.select([s], [], [], 1)
                if ready[0]:
                    # data, addr = mysocket.recv(1024)
                    data, addr = s.recvfrom(1024)
                    data = Layer5.parse_l5(data).payload
                    data = decrypt(data, sk)
                    print('\nMessage recived from ', addr, ': ', data)
            except Exception as e:
                print (e, 'Terminating server ...')
                break

        s.close()
        print ('Closed the server socket')
        print ('Terminating ...')

class RoutingSender(multiprocessing.Process):

    def __init__(self, address, port):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port


    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.address, self.port))

        message = "Hello from Routing!!"
        message = encrypt(message, pk).encode()
        message = bytes(Layer5(message))

        try:
            s.sendall(message)
        except Exception as e:
            print (e, 'Terminating server ...')
