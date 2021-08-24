import json
import os
from typing import Dict


class FileIO:
    def __init__(self):
        self.data = ""
        self.text = ""

    def open_json(self, file: str) -> Dict[str, str]:
        with open(file) as f:
            self.data = json.load(f)
        return self.data

    def open_text(self, file: str) -> str:
        """
        Read a textfile and ignore comments (#)
        :param file: path to file
        :return: file contents
        """
        try:
            if file.endswith(".txt"):
                self.text = ""
                with open(os.path.join(os.getcwd(), file), "r") as f:
                    for line in f:
                        if line.startswith("#"):
                            continue
                        self.text += line
                    return self.text
        except TypeError:
            raise TypeError("Invalid file extension. Must be .txt")

    def write_txt_file(self, path: str, filename: str, data: str) -> str:
        if path[-1] != "/":
            path += "/"
        full_path = path + filename
        self.data = str(data)
        open(full_path, "w").write(self.data)

        return full_path
