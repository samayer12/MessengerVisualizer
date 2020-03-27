import unittest
from unittest.mock import Mock, patch
from src.Visualizer import Visualizer
import src.Main


class MyTestCase(unittest.TestCase):
    @patch.object(Visualizer, 'plot_frequency')
    def test_plot_frequency_called_twice(self, mock):
        src.Main.graphData("Conversation")
        self.assertEqual(2, mock.call_count)

    @patch.object(Visualizer, 'plot_word_frequency')
    def test_plot_word_frequency_called_once(self, mock):
        src.Main.graphData("Conversation")
        self.assertEqual(1, mock.call_count)

if __name__ == '__main__':
    unittest.main()
