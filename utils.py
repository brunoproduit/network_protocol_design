import os, re, uuid, json, ipaddress, struct, socket, hashlib
from constants import *

class Utils:
    def __init__(self):
        self.data = []

    # Helper function to read a file returns a binary string
    # @param:filename string
    # @return: binary string
    def read_file(filename):
         if os.path.exists(filename):
             f = open(filename, 'rb')
             data = f.read()
             f.close()
             return data
         else:
            return False

    @staticmethod
    def read_neighbors_from_neighborfile():
        with open(NEIGHBORSFILE) as fn:
            line = fn.readline().rstrip()
            neighborlist = []

            while line:
                elem = line.split('=')
                if(Utils.valid_ip(elem[1])): # We don't care about the md5 hash
                    neighborlist.append((elem[0], elem[1]))
                line = fn.readline().rstrip()
        return neighborlist


    # Function to write a file as binary string
    # @param:filename string
    # @param:directory string
    # @param:data binary string
    # @param:overwrite boolean
    def write_file(filename, directory, data, overwrite = False):
        if os.path.exists(directory+ "/" + filename) and not overwrite:
            print('File already exist, choosing random name...')
            elements = filename.split(".")
            filename = str(uuid.uuid4())
            if len(elements) > 1:
                extension = elements[-1]
                filename = filename + "." + extension

        f = open(directory + "/" + filename,'wb') #open in binary
        f.write(data)
        f.close()
        print("File was written to " + directory + "/" + filename)

    # dumps the settings into a json
    def save_settings(self, settings):
        settingsContent = ""
        for setting in settings:
            settingsContent += setting + "=" + settings[setting].keypath + "\n"

        # json.dumps(settings.__dict__).encode(),
        Utils.write_file(
            SETTINGSFILE,
            ".",
            settingsContent.encode(),
            True
        )

    @staticmethod
    def valid_destination(address):
        return Utils.valid_mail(address) or address == BROADCAST_MAIL or Utils.valid_mail(address[1:]) or address == BROADCAST_MAIL[1:]

    @staticmethod
    def valid_mail(address):
        return re.match(r"[^@]+@[^@]+\.[^@]+", address)

    @staticmethod
    def address_to_md5(address):

        if address != BROADCAST_MAIL:
            if address.startswith('@'):  # remove first character if it's the @-sign!
                address = address[1:]
            m = hashlib.md5()
            m.update(str.encode(address))
            return m.hexdigest()
        else:
            return 32 * '0'

    @staticmethod
    def valid_ip(address):
        try:
            return ipaddress.IPv4Address(address)
        except:
            return False

    @staticmethod
    def int_to_bytestring(i, length):
        s = ""
        for _ in range(length):
            s = chr(i & 0xff) + s
            i >>= 8
        return s

    @staticmethod
    def hex_decode(bytes_in):
        s = ''
        for b in bytes_in:
            s += "%0.2X" % b
        return s

    @staticmethod
    def print_new_chat_line(output):
        print(output, '\nchat$')

    @staticmethod
    def dbg_log(message_list):
        if DEBUG:
            msg = ''
            for item in message_list:
                msg += str(item)
            print(msg)

# utils = Utils()
# pgpsettings = PGPSettings(MASTERKEYPATH, SOURCEKEYPATH)
# # write_file("test.txt", "..", b"Test!")
# print(read_file("../test.txt"))
# utils.save_settings(pgpsettings)
# utils.getNeighbors()
