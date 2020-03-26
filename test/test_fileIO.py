import unittest
import json
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
        self.assertRaises(TypeError, self.f.open_text(badfile))

    def test_open_text_AcceptsTxtFile(self):
        goodfile = 'TextInput/uncommentedwordlist.txt'
        self.assertIsNotNone(self.f.open_text(goodfile))


if __name__ == '__main__':
    unittest.main()
