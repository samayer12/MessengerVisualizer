import unittest
from unittest.mock import Mock, patch
from src.Visualizer import Visualizer
import src.Main


class MyTestCase(unittest.TestCase):
    @patch.object(Visualizer, 'plot_frequency')
    def test_plot_frequency_called_once(self, mock):
        src.Main.graphData()
        self.assertTrue(mock.called)


if __name__ == '__main__':
    unittest.main()
