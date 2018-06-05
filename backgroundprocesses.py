import select
import socket
import threading

from constants import *
from crypto import *


from packetEngine import PacketAccumulator, MessageAggregator


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

        msg_aggregator = MessageAggregator(self.sk)

        # Receive loop
        while True:
            try:
                ready = select.select([s], [], [], 1)
                if ready[0]:
                    data, addr = s.recvfrom(1024)
                    msg_aggregator.feed_packet(data)
                
                # Print any finalized messages.
                msg_aggregator.print_ready()
            except Exception as e:
                print("Exception in listener: ", e)
        s.close()
        print('Closed the server socket')
        print('Terminating ...')
