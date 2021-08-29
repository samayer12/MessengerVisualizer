import json
import io
import os
import unittest
from unittest import mock
from unittest.mock import patch

from src.FileIO import FileIO


class FileIOTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.f = FileIO()

    def tearDown(self):
        del self.f

    def test_OpenSpecifiedFileInSubDir(self):
        with open("test/Messages/message.json") as file:
            expected_json = json.load(file)
            result = self.f.open_json("test/Messages/message.json")
            self.assertEqual(expected_json, result)
            self.assertGreater(self.f.data.__len__(), 0)

    def test_open_text_StripsCommentsFromTxtFiles(self):
        uncommented = self.f.open_text("test/TextInput/uncommentedwordlist.txt")
        commented = self.f.open_text("test/TextInput/commentedwordlist.txt")

        self.assertEqual(uncommented, commented)

    @patch('os.path.isfile', return_value=True)
    def test_open_text_RejectsNonTxtFile(self, stub_isfile):
        badfile = "bad.doc"
        with self.assertRaises(TypeError) as exception_context:
            self.f.open_text(badfile)
            stub_isfile.assert_called()
            self.assertTrue('Invalid file extension. Must be .txt' in exception_context.exception)

    @patch('os.path.isfile', return_value=True)
    def test_open_text_AcceptsTxtFile_Mocked(self, stub_isfile):
        fake_file = io.StringIO("Mocked\nOutput")
        with mock.patch("src.FileIO.open", return_value=fake_file, create=True):
            result = self.f.open_text("/path/to/good.txt")
            self.assertEqual("Mocked\nOutput", result)
        stub_isfile.assert_called()

    @patch("builtins.open")
    def test_write_file_directory_adds_slash_to_path(self, mock_open):
        fake_directory = "/path/to/dir"
        self.f.write_txt_file(fake_directory, "file.txt", "Data")
        mock_open.assert_called_once_with("/path/to/dir/file.txt", "w")

    @patch("builtins.open")
    def test_write_file_directory_accepts_existing_slash(self, mock_open):
        fake_directory = "/path/to/dir/"
        self.f.write_txt_file(fake_directory, "file.txt", "Data")
        mock_open.assert_called_once_with("/path/to/dir/file.txt", "w")

    @patch("builtins.open")
    def test_write_file_writes_text_data(self, mock_creation):
        fake_data = "Data"
        self.f.write_txt_file("/path/to/dir", "file.txt", fake_data)

        mock_creation.assert_called_once_with("/path/to/dir/file.txt", "w")
        mock_creation().write.assert_called_once_with("Data")

    @patch("builtins.open")
    def test_write_file_writes_dict_data(self, mock_creation):
        fake_data = {"Data"}
        self.f.write_txt_file("/path/to/dir", "file.txt", fake_data)

        mock_creation.assert_called_once_with("/path/to/dir/file.txt", "w")
        mock_creation().write.assert_called_once_with("{'Data'}")

    def test_validate_directory_accepts_directories(self):
        result = FileIO.validate_directory(os.getcwd())
        self.assertEqual(f'{os.getcwd()}/', result)

    def test_validate_directory_rejects_file(self):
        with self.assertRaises(NotADirectoryError) as exception_context:
            FileIO.validate_directory('/test/path/file.txt')
            self.assertTrue('must be a directory' in exception_context.exception)


if __name__ == "__main__":
    unittest.main()
