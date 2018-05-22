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
            
    def read(filename):
        with open(filename) as fn:
            line = fn.readline().rstrip()
            dictionary = "{"
            elem = line.split('=')
            dictionary = dictionary + "\"" + elem[0] + "\"" + ":" + "\"" + elem[1] + "\""
            while line:
                line = fn.readline().rstrip()
                if line != "" :
                    elem = line.split('=')
                    dictionary = dictionary + ", \"" + elem[0] + "\"" + ":" + "\"" + elem[1] + "\""
        dictionary = dictionary + "}"
        return dictionary


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

    def valid_destination(self, address):
        return self.valid_mail(address) or address == BROADCAST_MAIL or self.valid_mail(address[1:]) or address == BROADCAST_MAIL[1:]

    def valid_mail(self, address):
        return re.match(r"[^@]+@[^@]+\.[^@]+", address)

    def address_to_md5(address):
        if address != BROADCAST_MAIL:
            m = hashlib.md5()
            m.update(str.encode(address))
            return m.hexdigest()
        else:
            return 32 * '0'

    def valid_ip(self, address):
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
    def bytes_to_int(bytes):
        result = 0
        for byte in bytes:
            result += result * 256 + int(byte)
        return result
    
    @staticmethod
    def hex_decode(bytes_in):
        s = ''
        for b in bytes_in:
            s += "%0.2X" % b
        return s

# utils = Utils()
# pgpsettings = PGPSettings(MASTERKEYPATH, SOURCEKEYPATH)
# # write_file("test.txt", "..", b"Test!")
# print(read_file("../test.txt"))
# utils.save_settings(pgpsettings)
# utils.getNeighbors()
