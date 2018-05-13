import json

class PGPSetting(json.JSONEncoder):

    # Constructor
    def __init__(self, keypath, keydata):
        self.keypath = keypath
        self.keydata = keydata
