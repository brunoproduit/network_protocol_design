import threading
import time

# from globals import *
# from command import Command
from constants import *
from globals import unconfirmed_message_queue

class ConfirmMessageThread(threading.Thread):
    def __init__(self, l3_message):
        threading.Thread.__init__(self)
        self.l3_message = l3_message

    def run(self):
        i = 0
        acked = False
        while i <= 15:
            i += 1
            time.sleep(2)  # 2 seconds

            # global unconfirmed_message_queue
            if self.l3_message.packet_number in unconfirmed_message_queue:
                print('LOG: Resending Message', self.l3_message.payload.payload.payload, ',', i, 'times already tried')
                # Command.execute(SEND_MESSAGE_COMMAND, self.l3_message)
            else:
                acked = True
                break
        print('LOG: Message ACK status:', acked)
        # global unconfirmed_message_queue
        # del unconfirmed_message_queue[self.l3_message.confirmation_id]
