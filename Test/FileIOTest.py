import unittest
from FileIO import FileIO


class FileIOTest(unittest.TestCase):
    def test_FileIORuns(self):
        self.assertEqual(FileIO.hello(self), "Hello")

    def test_OpenSpecifiedFileInSubDir(self):
        f = FileIO()
        self.assertEqual(f.open_file('Messages\Erin\message.json'), 'Messages\Erin\message.json')
        self.assertGreater(f.data.__len__(), 0)
