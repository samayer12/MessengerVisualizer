import json
import io
import unittest
import unittest.mock as mock


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

# Test for with/without trailing '/' in FileIO
    def test_write_file_directory_adds_slash(self):
        fake_directory = '/path/to/dir'
        result = self.f.write_txt_file(fake_directory, 'file.txt', "Data")
        self.assertEqual('/path/to/dir/file.txt', result)

    def test_write_file_directory_accepts_existing_slash(self):
        fake_directory = '/path/to/dir/'
        result = self.f.write_txt_file(fake_directory, 'file.txt', "Data")
        self.assertEqual('/path/to/dir/file.txt', result)


# Test for text input
# Test for Dict input
# Test for Counter() input

if __name__ == '__main__':
    unittest.main()
