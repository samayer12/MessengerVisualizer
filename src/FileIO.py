import json
import os


class FileIO:

    def __init__(self):
        self.data = ""
        self.text = ""

    def open_json(self, file):
        with open(file) as f:
            self.data = json.load(f)
        return self.data

    def open_text(self, file):
        try:
            if file.endswith('.txt'):
                self.text = ""
                with open(os.path.join(os.getcwd(), file), 'r') as f:
                    for line in f:
                        if line.startswith('#'):
                            continue
                        self.text += line
                    return self.text
        except TypeError:
            raise TypeError('Invalid file extension. Must be .txt')

    def write_txt_file(self, path, filename, data):
        if path[-1] != '/':
            path += '/'
        full_path = path + filename
        open(full_path, 'w').write(data)

        return full_path
