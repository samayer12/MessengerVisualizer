import unittest

import matplotlib

from src.Visualizer import *


class VisualizationTest(unittest.TestCase):
    def test_strip_specified_words(self):
        words = ['soft', 'ship', 'slippery', 'sulky', 'useless', 'talk', 'interesting', 'hideous', 'stay',
                 'back', 'royal', 'hope']
        wordlist = ['back', 'royal', 'hope', 'useless', 'talk', 'interesting', 'hideous']
        self.assertNotIn(strip_common(words, wordlist), wordlist)

    def test_plot_frequency_returns_a_graph(self):
        fake_data = {'0': 1, '1': 2}
        assert type(Visualizer.plot_frequency('Fake Graph', 'x', 'y', fake_data)) is matplotlib.container.BarContainer
if __name__ == '__main__':
    unittest.main()
