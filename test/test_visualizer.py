import unittest
from src.Visualizer import *


class VisualizationTest(unittest.TestCase):
    def test_strip_specified_words(self):
        words = ['soft', 'ship', 'slippery', 'sulky', 'useless', 'talk', 'interesting', 'hideous', 'stay',
                 'back', 'royal', 'hope']
        wordlist = ['back', 'royal', 'hope', 'useless', 'talk', 'interesting', 'hideous']
        self.assertNotIn(Visualizer.strip_common(wordlist), wordlist)


if __name__ == '__main__':
    unittest.main()
