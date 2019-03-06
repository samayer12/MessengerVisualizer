import json


class FileIO:
    data = ""

    def __init__(self):
        print("File IO starting\n ")

    def hello(self):
        return "Hello"

    def open_file(self, file):
        with open(file) as f:
            self.data = json.load(f)
        return self.data
