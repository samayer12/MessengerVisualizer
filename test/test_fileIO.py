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
        self.assertEqual(self.f.open_json('Messages/message.json'), json.load(open('Messages/message.json')))
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

if __name__ == '__main__':
    unittest.main()
