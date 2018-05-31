import multiprocessing
import select
import socket

from constants import *
from crypto import *
from layer3 import *
from layer4 import *
from layer5 import *

# Thread instead of process
from packetEngine import PacketAccumulator, MessageAggregator


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

        msg_aggregator = MessageAggregator(self.sk)

        # Receive loop
        while True:
            try:
                ready = select.select([s], [], [], 1)
                if ready[0]:
                    data, addr = s.recvfrom(1024)
                    msg_aggregator.feed_packet(data)
                    msg_aggregator.print_ready()
            except Exception as e:
                print("Exception in listener: ", e)
        s.close()
        print ('Closed the server socket')
        print ('Terminating ...')
