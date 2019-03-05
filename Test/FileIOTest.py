import unittest
from FileIO import FileIO


def fun(x):
    return x + 1


class FileIOTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

    def FileIORuns(self):
        self.assertEqual(FileIO.hello(self), "Hello")

    def OpenSpecifiedFileInSubDir(self):
        f = FileIO()
        self.assertEqual(f.openFile('Messages\Erin\message.json'), 'Messages\Erin\message.json')
        self.assertGreater(f.data.__len__(), 0)