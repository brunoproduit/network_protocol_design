import os, uuid, json
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

    # def readSettings(self, filename):

    # router.neighbours[md5hash]
    # TODO: SendMessage, SaveSettings, SendUsermessage

utils = Utils()
pgpsettings = PGPSettings(MASTERKEYPATH, SOURCEKEYPATH)
# utils.writeFile("test.txt", "..", b"Test!")
print(utils.readFile("../test.txt"))
utils.saveSettings(pgpsettings)
