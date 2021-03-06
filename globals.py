from utils import *
from threading import Lock

print('Reading in neighbors from ', NEIGHBORSFILE)
neighbors = Utils.read_neighbors_from_neighborfile()
print(neighbors)
print('Finished reading neighbors')

global router
router = Router(source_address, neighbors)
packet_number_counter = 1024

global unconfirmed_message_queue
unconfirmed_message_queue = set([])

lock = Lock()

# Thread-safe add to unconfirmed queue.
def add_unconfimed_message(id):
    global unconfirmed_message_queue
    lock.acquire()
    unconfirmed_message_queue.add(id)
    lock.release()

# Thread-safe delete from unconfirmed queue if present.
def del_unconfimed_message(id):
    global unconfirmed_message_queue
    lock.acquire()
    unconfirmed_message_queue.discard(id)
    lock.release()

# Thread-safe item check in unconfirmed queue.
def is_unconfimed_message(id):
    global unconfirmed_message_queue
    lock.acquire()
    is_present = id in unconfirmed_message_queue
    lock.release()
    return is_present

def get_next_packet_number():
    global packet_number_counter
    packet_number_counter += 1
    if(packet_number_counter == 2147483647):
        packet_number_counter = 0
    return packet_number_counter