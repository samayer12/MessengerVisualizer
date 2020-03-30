import unittest
from unittest.mock import patch
import src.Main


class MainTestCases(unittest.TestCase):
    @patch('src.Visualizer.Visualizer.plot_frequency')
    @patch('src.Visualizer.Visualizer.plot_word_frequency')
    def test_plot_methods_called_correct_number_of_times(self, mock_word_frequency, mock_frequency):
        src.Main.graphData("data")
        self.assertEqual(1, mock_word_frequency.call_count)
        self.assertEqual(2, mock_frequency.call_count)


if __name__ == '__main__':
    unittest.main()
