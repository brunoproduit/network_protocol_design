import os, re, uuid, json, ipaddress, struct, socket, hashlib
from settings import *
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
        write_file(
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
            return 16 * '0'

    def valid_ip(self, address):
        try:
            return ipaddress.IPv4Address(address)
        except:
            return False

    def int_to_bytestring(i, length):
        s = ""
        for _ in range(length):
            s = chr(i & 0xff) + s
            i >>= 8
        return s

    def bytes_to_int(bytes):
        result = 0
        for byte in bytes:
            result += result * 256 + int(byte)
        return result

    def to_hexstring(hex):
        string = ''
        hex[0] + hex[1]
        i = 2
        while i < len(hex):
            string += 'x' + hex[i] + hex[i+1]
            i+=2
        # return string.replace('x', '\x')


# utils = Utils()
# pgpsettings = PGPSettings(MASTERKEYPATH, SOURCEKEYPATH)
# # write_file("test.txt", "..", b"Test!")
# print(read_file("../test.txt"))
# utils.save_settings(pgpsettings)
# utils.getNeighbors()
