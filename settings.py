import json

class PGPSettings(json.JSONEncoder):

    # Constructor
    def __init__(self, masterkeypath, sourcekeypath):
        self.masterkeypath = masterkeypath
        self.sourcekeypath = sourcekeypath
