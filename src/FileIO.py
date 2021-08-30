import json
import logging
import os
from typing import Dict

fileio_logger = logging.getLogger('MessengerViz.fileIO')

class FileIO:
    def __init__(self):
        self.logger = logging.getLogger('MessengerViz.fileIO.FileIO')
        self.data = ""
        self.text = ""

    def open_json(self, file: str) -> Dict[str, str]:
        self.logger.debug('Opening: %s', file)
        with open(file) as f:
            self.data = json.load(f)
        self.logger.debug('Finished reading: %s', file)
        return self.data

    def open_text(self, file: str) -> str:
        """
        Read a textfile and ignore comments (#)
        :param file: path to file
        :return: file contents
        """
        if not os.path.isfile(file):
            raise FileNotFoundError('Could not locate %s', file)
        if file.endswith(".txt"):
            self.text = ""
            self.logger.debug('Opening: %s', file)
            with open(os.path.join(os.getcwd(), file), "r") as f:
                for line in f:
                    if line.startswith("#"):
                        continue
                    self.text += line
                self.logger.debug('Finished reading: %s', file)
                return self.text
        else:
            raise TypeError("Invalid file extension. Must be .txt")

    def write_txt_file(self, path: str, filename: str, data: str) -> str:
        full_path = FileIO.validate_directory(path) + filename
        self.data = str(data)
        self.logger.debug('Writing contents to: %s', full_path)
        open(full_path, "w").write(self.data)
        self.logger.debug('Finished writing to: %s', full_path)

        return full_path

    @staticmethod
    def validate_directory(path: str) -> str:
        """
        Make sure filepaths have a trailing slash
        :param path: Path to validate
        :return: A path, ending in '/`
        """
        if os.path.isdir(path):
            return os.path.join(path, '')
        else:
            raise NotADirectoryError("Input must be a directory")
