from layer3 import *
from layer4 import *
from layer5 import *
from crypto import *
from globals import router
from datetime import datetime, timedelta
import time
from constants import *
import threading
import socket


# Sends a packet and awaits for the ACK. Resends if no ACK.
class ThreadedSender:
    def __init__(self, l3_data):
        self.l3_data = l3_data
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global router
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address_tuple = router.get_next_hop(self.l3_data.destination.hex())

        if address_tuple is not None:
            ip_address = address_tuple[1]
            s.connect((ip_address, PORT))  # PORT could also be used somewhere else!
            try:
                s.sendall(bytes(self.l3_data))
            except Exception as e:
                print(e, 'Terminating server ...')
        else:
            print(self.l3_data.destination.hex(), ', doesn\'t exist in the neighbors list, try another Mail!')
            return

        # while True:
            # Wait for the ACK here.
            # TODO: wait for ACK, resend if none
            # time.sleep()

# Outgoing stream manager.
class StreamManager:
    def __init__(self, pk):
        # self.dividers = []  # TODO: Add control of the operations here.
        # self.occupied_ids = []
        self.pk = pk
        self.current_id = 0
    
    def get_next_stream_id(self):
        self.current_id += 1
        # TODO: restart loop
        # TODO: mark unoccupied when freed
        return self.current_id

    def add_stream(self, source, destination, data, is_file=False, file_name=""):
        size = len(data)
        index = 0
        chunk_id = 0
        stream_id = self.get_next_stream_id()

        print("Size: ", size)
        
        while index < size:
            stop_bit = False
            if index + MAX_PDU_SIZE <= size:
                chunk = data[index:index + MAX_PDU_SIZE]
            else:
                chunk = data[index:size]

            if index + MAX_PDU_SIZE >= size:
                stop_bit = True

            index += MAX_PDU_SIZE

            source_address = Utils.address_to_md5(source)
            destination_address = Utils.address_to_md5(destination)

            l3_packet = Layer3(
                Layer4(
                    Layer5(
                        encrypt(chunk, self.pk).encode() if not is_file else encrypt_file(file_name + '\00' + chunk, self.pk).encode(), 
                        L5_MESSAGE if not is_file else L5_FILE),
                    L4_DATA, 
                    True,
                    True, 
                    1 if stop_bit else 0, #  TODO: Check status format in spec.
                    stream_id, 
                    chunk_id),
                bytes.fromhex(source_address),
                bytes.fromhex(destination_address),
                0, #  TODO: Packet number?
                packet_type=L3_DATA)

            # Debug
            # print(chunk, ' ', stream_id, ' ', chunk_id, ' ', stop_bit)

            chunk_id += 1
            ThreadedSender(l3_packet)


# Assembles single stream from incoming packets.
class PacketAccumulator:
    def __init__(self, sk):
        self.finished = False
        self.finished_time = datetime.now()
        self.stream_id = 0
        self.data = {}
        self.sk = sk

    def accumulate(self, raw_data):
        try:
            l3_data = Layer3.parse_l3(raw_data)
            l4_data = l3_data.payload
            l5_data = l3_data.payload.payload
        except Exception as e:
            print("Error accumulating packet: " + str(e))
            return

        if self.stream_id == 0:
            self.stream_id = l4_data.stream_id
        elif self.stream_id != l4_data.stream_id:
            print("Wrong stream ID!")
            return

        if l4_data.status == 1:
            self.finished = True
            self.finished_time = datetime.now()

        if l5_data.type.encode() == L5_MESSAGE:
            self.data[l4_data.chunk_id] = decrypt(l5_data.payload, self.sk)
            # Debug
            # print("MsgPart ", l3_data.source, ': ', self.data[l4_data.chunk_id], " (stream/chunk ", self.stream_id, "/", l4_data.chunk_id, ")")
        elif l5_data.type.encode() == L5_FILE:
            print("FilePart ", l4_data.chunk_id)
            # TODO: Files
        else:
            print("Invalid packet type")

        # TODO: Send ACK

    def check(self):
        if self.finished:             
            # Check integrity
            combined_data = '' # TODO: File also!
            start_id = -1
            for key, value in sorted(self.data.items()):
                if key - start_id != 1:
                    if datetime.now() > self.finished_time + timedelta(0, 20):
                        return MSG_NOTREADY
                    # else:
                    #    print("Packet receving timed out...")
                    #    return MSG_TIMEOUT
                
                combined_data += value
            print(combined_data)
            return MSG_READY
        return MSG_NOTREADY


# Incoming stream manager.
class MessageAggregator:
    def __init__(self, sk):
        self.accumulators = []
        self.sk = sk

    # Feed a random packet to aggregator.
    def feed_packet(self, packet):
        try:
            stream_id = Layer3.parse_l3(packet).payload.stream_id
        except Exception as e:
            print(e)
            return
        
        self.insert(stream_id, packet)

    def insert(self, stream, packet):
        for accumulator in self.accumulators:
            if accumulator.stream_id == stream:
                accumulator.accumulate(packet)
                return

        accumulator = PacketAccumulator(self.sk)
        accumulator.accumulate(packet)
        self.accumulators.append(accumulator)

    # Check all the accumulators and see if any of them are ready.
    def print_ready(self):
        for a in self.accumulators:
            state = a.check()
            if state == MSG_READY or state == MSG_TIMEOUT:
                self.accumulators.remove(a)
