import os, uuid, json, ipaddress, struct, socket
from settings import *
from constants import *

class Utils:
    def __init__(self):
        self.data = []

    # Helper function to read a file returns a binary string
    # @param:filename string
    # @return: binary string
    def readFile(self, filename):
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
        settingsContent = ""
        for setting in settings:
            settingsContent += setting + "=" + settings[setting].keypath + "\n"

        # json.dumps(settings.__dict__).encode(),
        self.writeFile(
            SETTINGSFILE,
            ".",
            settingsContent.encode(),
            True
        )

    # TODO: get settings from settingsfile --> then dont ask for new settings!
    # def readSettings(self, filename):
    def getNeighbors(self):
        print("Do something, tell me your neighbours, arrr!")
        addmore = 'y'
        neighbors = {}
        while inp.lower() == 'y':
            ip = input('Tell me your neighbor\'s IP: ') # TODO: do a check if it even is an IP!
            mail = input('Tell me your neighbor\'s email: ') # TODO: cast to md5!
            neighbors[mail] = self.ip2int(ip)
            addmore = input('Add more neighbors? y/n ')
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
# utils.getNeighbors()
