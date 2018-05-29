from utils import *

print('Reading in neighbors from ', NEIGHBORSFILE)
neighbors = Utils.read_neighbors_from_neighborfile()
print(neighbors)
print('Finished reading neighbors')

global router
router = Router(source_address, neighbors)
packet_number_counter = 0

global unconfirmed_message_queue
unconfirmed_message_queue = []

def get_next_packet_number():
    packet_number_counter =+ 1
    if(packet_number_counter == 2147483647):
        packet_number_counter = 0
    return packet_number_counter