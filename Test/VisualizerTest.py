import unittest, json
from Visualizer import *
from FileIO import FileIO

class VisualizationTest(unittest.TestCase):
    def test_strip_specified_words(self):
        words = ['soft', 'ship', 'slippery', 'sulky', 'useless', 'talk', 'interesting', 'hideous', 'stay',
                 'back', 'royal', 'hope']
        wordlist = ['back', 'royal', 'hope', 'useless', 'talk', 'interesting', 'hideous']
        self.assertNotIn(strip_common(words, wordlist), wordlist)
