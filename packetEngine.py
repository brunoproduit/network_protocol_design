from layer3 import *
from layer4 import *
from layer5 import *
from crypto import *
from globals import *
from datetime import datetime, timedelta
import time
from constants import *
from utils import Utils
import threading
import socket


# Sends a packet and awaits for the ACK. Resends if no ACK.
class ThreadedSender:
    def __init__(self, l3_data, broadcast_address = None):
        self.l3_data = l3_data
        self.broadcast_address = broadcast_address
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global router
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.broadcast_address is None:
            address_tuple = router.get_next_hop(self.l3_data.destination.hex())
        else:
            address_tuple = (BROADCAST_ADDRESS, self.broadcast_address)

        if address_tuple is not None:
            ip_address = address_tuple[1]
            s.connect((ip_address, PORT))  # PORT could also be used somewhere else!
            try:
                s.sendall(bytes(self.l3_data))
                add_unconfimed_message(self.l3_data.packet_number)
            except Exception as e:
                print('Exception sending packet...', e)
        else:
            print(self.l3_data.destination.hex(), ', doesn\'t exist in the neighbors list, try another Mail!')
            return

        tries = 0
        while tries < SEND_RETRIES:
            time.sleep(ACK_TIMEOUT)
            if is_unconfimed_message(self.l3_data.packet_number):
                Utils.dbg_log(["Packet unconfirmed ", self.l3_data.packet_number, ", re-send!"])
                tries += 1
                try:
                    s.sendall(bytes(self.l3_data))
                except Exception as e:
                    print('Exception re-sending packet...', e)
            else:
                Utils.dbg_log(["Confirmation received by sender ", self.l3_data.packet_number])
                return
        
        print("Error: Packet not delivered", self.l3_data.packet_number)

# Outgoing stream manager.
class StreamManager:
    def __init__(self, pk):
        self.pk = pk
        self.current_id = 0
    
    def get_next_stream_id(self):
        self.current_id += 1
        if self.current_id == 2147483647:
            self.current_id = 0
        return self.current_id

    def add_stream(self, source, destination, data, is_file=False, file_name=""):
        if is_file:
            data = file_name + '\00' + encrypt_file(data, self.pk)

        size = len(data)
        index = 0
        chunk_id = 0
        stream_id = self.get_next_stream_id()
        
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
                        encrypt(chunk, self.pk),
                        L5_MESSAGE if not is_file else L5_FILE),
                    L4_DATA, 
                    True,
                    True, 
                    1 if stop_bit else 0, 
                    stream_id, 
                    chunk_id),
                bytes.fromhex(source_address),
                bytes.fromhex(destination_address),
                get_next_packet_number(),
                packet_type=L3_DATA)

            # Utils.dbg_log([chunk, ' ', stream_id, ' ', chunk_id, ' ', stop_bit])

            chunk_id += 1

            if l3_packet.destination.hex() != BROADCAST_ADDRESS:
                ThreadedSender(l3_packet)
            else:
                for node in router.neighbors:
                    ThreadedSender(l3_packet, node[1])
                    l3_packet.packet_number = get_next_packet_number()


# Assembles single stream from incoming packets.
class PacketAccumulator:
    def __init__(self, sk):
        self.finished = False
        self.finished_time = datetime.now()
        self.stream_id = 0
        self.data = {}
        self.sk = sk
        self.sender = ""
        self.is_file = False

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
            self.sender = l3_data.source
            self.is_file = False if l5_data.type == L5_MESSAGE else True
        elif self.stream_id != l4_data.stream_id:
            print("Wrong stream ID!")
            return

        if l4_data.status == 1:
            self.finished = True
            self.finished_time = datetime.now()

        self.data[l4_data.chunk_id] = decrypt(l5_data.payload, self.sk)
        if l5_data.type == L5_MESSAGE:
            Utils.dbg_log(["MsgPart ", l3_data.source, ': ', self.data[l4_data.chunk_id], " (stream/chunk ", self.stream_id, "/", l4_data.chunk_id, ")"])
        elif l5_data.type == L5_FILE:
            Utils.dbg_log(["FilePart ", l3_data.source, 
                " (stream/chunk ", self.stream_id, "/", l4_data.chunk_id, " packet ",
                l3_data.packet_number, ")"])
        else:
            print("Invalid packet type")

        # Send ACK.
        ack_message = Layer3(
            Layer4(Layer5(b''), L4_DATA),
            l3_data.destination,
            l3_data.source,
            get_next_packet_number(),
            15, 
            L3_CONFIRMATION, 
            l3_data.packet_number)

        global router
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address_tuple = router.get_next_hop(ack_message.destination.hex())

        if address_tuple is not None:
            ip_address = address_tuple[1]
            s.connect((ip_address, PORT))  # PORT could also be used somewhere else!
            try:
                s.sendall(bytes(ack_message))
            except Exception as e:
                print('Exception sending ACK packet...', e)

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

            if not self.is_file:
                print(self.sender.hex(), ": ", combined_data)
            else:
                file_name = combined_data[0:combined_data.find('\00')]
                print(self.sender.hex(), " sent file '", file_name, "'")
                Utils.write_file(file_name, '.', decrypt(combined_data[combined_data.find('\00')+1:], self.sk).encode())
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
            l3_data = Layer3.parse_l3(packet)
        except Exception as e:
            print(e)
            return

        try:
            if l3_data.type == L3_CONFIRMATION:
                if is_unconfimed_message(l3_data.confirmation_id):
                    del_unconfimed_message(l3_data.confirmation_id)
                    Utils.dbg_log(["Confirmed by receiver ", l3_data.confirmation_id])
                else:
                    Utils.dbg_log(["Packet already confirmed ", l3_data.confirmation_id])
                    # pass
                return
            
            stream_id = l3_data.payload.stream_id
            self.insert(stream_id, packet)
        except Exception as e:
            print("Failed to feed a packet:", e)

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
