import json, os
from pprint import pprint

class FileIO:

    filesize = 0
    data = ""

    def __init__(self):
        print("File IO starting")

    def hello(self):
        return "Hello"

    def openFile(self, file):
        with open(file) as f:
            self.data = json.load(f)
        return file
