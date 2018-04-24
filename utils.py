import os, uuid, json, ipaddress, struct, socket
from settings import PGPSettings
from constants import *

class Utils:
    def __init__(self):
        self.data = []

    # Helper function to read a file returns a binary string
    # @param:filefilename string
    # @return: binary string
    def readFile(self, filefilename):
         if os.path.exists(filefilename):
             f = open(filefilename, 'rb')
             data = f.read()
             f.close()
             return data
         else:
            return False

    # Function to write a file as binary string
    # @param:filename string
    # @param:directory string
    # @param:data binary string
    def writeFile(self, filename, directory, data, overwrite = False):
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
    def saveSettings(self, settings):
        self.writeFile(
            SETTINGSGILE,
            ".",
            json.dumps(settings.__dict__).encode(),
            True
        )

    # TODO: get settings from settingsfile --> then dont ask for new settings!
    # def readSettings(self, filename):
    def setNeighbors(self):
        print("Do something, get neighbours, arrr!")
        inp = 'y'
        neighbors = {}
        while inp.lower() == 'y':
            ip = input('Tell me your neighbors IP: ')
            mail = input('Tell me your neighbors email: ')
            neighbors[mail] = self.ip2int(ip)
            inp = input('Add more neighbors? y/n ')
        print("neigbours given:", neighbors)
        return neighbors

    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]


    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

    # router.neighbours[md5hash]
    # TODO: SendMessage, SaveSettings, SendUsermessage

# utils = Utils()
# pgpsettings = PGPSettings(MASTERKEYPATH, SOURCEKEYPATH)
# # utils.writeFile("test.txt", "..", b"Test!")
# print(utils.readFile("../test.txt"))
# utils.saveSettings(pgpsettings)
# utils.setNeighbors()
