import unittest
from unittest.mock import patch, DEFAULT
import src.Main


class MainTestCases(unittest.TestCase):
    @patch('src.Conversation')
    @patch('src.Visualizer.Visualizer.plot_frequency', return_value="Graph1")
    @patch('src.Visualizer.Visualizer.plot_word_frequency', return_value="Graph2")
    def test_plot_methods_called_correct_number_of_times(self, mock_word_frequency, mock_frequency, mock_conversation):
        src.Main.graphData(mock_conversation, wordlist=None)
        self.assertEqual(1, mock_word_frequency.call_count)
        self.assertEqual(2, mock_frequency.call_count)

    @patch('src.Conversation')
    @patch('builtins.print')
    def test_message_print_called_correct_number_of_times(self, mock_print, mock_conversation):
        src.Main.printMessages(mock_conversation)
        self.assertEqual(3, mock_print.call_count)


if __name__ == '__main__':
    unittest.main()
