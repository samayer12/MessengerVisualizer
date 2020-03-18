import json, os


class FileIO:
    data = ""

    def __init__(self):
        print("File IO starting\n ")

    def hello(self):
        return "Hello"

    def open_json(self, file):
        with open(file) as f:
            self.data = json.load(f)
        return self.data

    def open_text(self, file):
        try:
            if file.endswith('.txt'):
                text = ""
                with open(os.path.join(os.getcwd(), file), 'r') as f:
                    for line in f:
                        if (line.startswith('#')):
                           continue
                        text += line
                    return text
        except TypeError:
            raise TypeError('Invalid file extension. Must be .txt');
