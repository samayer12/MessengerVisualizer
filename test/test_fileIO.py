import unittest, json
from src.FileIO import FileIO


class FileIOTest(unittest.TestCase):
    def test_FileIORuns(self):
        self.assertEqual(FileIO.hello(self), "Hello")

    def test_OpenSpecifiedFileInSubDir(self):
        f = FileIO()
        self.assertEqual(f.open_json('Messages/message.json'), json.load(open('Messages/message.json')))
        self.assertGreater(f.data.__len__(), 0)

    def test_open_text_StripsCommentsFromTxtFiles(self):
        f = FileIO()
        uncommented = f.open_text('TextInput/uncommentedwordlist.txt')
        commented = f.open_text('TextInput/commentedwordlist.txt')

        self.assertEqual(uncommented, commented)

    def test_open_text_RejectsNonTxtFile(self):
        f = FileIO()
        badfile = "bad.doc"
        self.assertRaises(TypeError, f.open_text(badfile))

    def test_open_text_AcceptsTxtFile(self):
        f = FileIO()
        goodfile = 'TextInput/uncommentedwordlist.txt'
        self.assertIsNotNone(f.open_text(goodfile))


if __name__ == '__main__':
    unittest.main()
