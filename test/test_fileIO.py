import json
import io
import unittest
from unittest import mock
from unittest.mock import patch


from src.FileIO import FileIO


class FileIOTest(unittest.TestCase):

    def setUp(self):
        self.f = FileIO()

    def tearDown(self):
        del self.f

    def test_OpenSpecifiedFileInSubDir(self):
        with open('Messages/message.json') as file:
            expected_json = json.load(file)
            result = self.f.open_json('Messages/message.json')
            self.assertEqual(expected_json, result)
            self.assertGreater(self.f.data.__len__(), 0)

    def test_open_text_StripsCommentsFromTxtFiles(self):
        uncommented = self.f.open_text('TextInput/uncommentedwordlist.txt')
        commented = self.f.open_text('TextInput/commentedwordlist.txt')

        self.assertEqual(uncommented, commented)

    def test_open_text_RejectsNonTxtFile(self):
        badfile = "bad.doc"
        result = self.f.open_text(badfile)
        self.assertRaises(TypeError, result)

    def test_open_text_AcceptsTxtFile_Mocked(self):
        fake_file = io.StringIO('Mocked\nOutput')
        with mock.patch('src.FileIO.open', return_value=fake_file, create=True):
            result = self.f.open_text('/path/to/good.txt')
            self.assertEqual('Mocked\nOutput', result)

    @patch('builtins.open')
    def test_write_file_directory_adds_slash_to_path(self, mock_open):
        fake_directory = '/path/to/dir'
        self.f.write_txt_file(fake_directory, 'file.txt', "Data")
        mock_open.assert_called_once_with('/path/to/dir/file.txt', 'w')

    @patch('builtins.open' )
    def test_write_file_directory_accepts_existing_slash(self, mock_open):
        fake_directory = '/path/to/dir/'
        self.f.write_txt_file(fake_directory, 'file.txt', "Data")
        mock_open.assert_called_once_with('/path/to/dir/file.txt', 'w')

    @patch('builtins.open')
    def test_write_file_writes_text_data(self, mock_creation):
        fake_data = 'Data'
        self.f.write_txt_file('/path/to/dir', 'file.txt', fake_data)

        mock_creation.assert_called_once_with('/path/to/dir/file.txt', 'w')
        mock_creation().write.assert_called_once_with('Data')

    @patch('builtins.open')
    def test_write_file_writes_dict_data(self, mock_creation):
        fake_data = {'Data'}
        self.f.write_txt_file('/path/to/dir', 'file.txt', fake_data)

        mock_creation.assert_called_once_with('/path/to/dir/file.txt', 'w')
        mock_creation().write.assert_called_once_with("{'Data'}")

    @patch('builtins.open')
    def test_write_file_writes_counter_data(self, mock_creation):
        from collections import Counter
        fake_data = Counter({'Data': 1})
        self.f.write_txt_file('/path/to/dir', 'file.txt', fake_data)

        mock_creation.assert_called_once_with('/path/to/dir/file.txt', 'w')
        mock_creation().write.assert_called_once_with("Counter({'Data': 1})")

if __name__ == '__main__':
    unittest.main()
