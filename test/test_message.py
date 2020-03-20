import unittest
from src.FileIO import FileIO
from src.Message import Message


class MessageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skeleton_JSON = FileIO()
        cls.skeleton_JSON.open_json('Messages/message_skeleton.json')
        cls.message = Message(cls.skeleton_JSON.data)

    @classmethod
    def tearDownClass(cls):
        del cls.skeleton_JSON
        del cls.message

    def test_parse_sender(self):
        self.assertEqual(self.message.sender_name, "Alice")

    def test_parse_timestamp(self):
        self.assertEqual(1535232149.475,
                         self.message.timestamp.timestamp())

    def test_parse_content(self):
        self.assertEqual(self.message.content, "Hello, Bob")

    def test_parse_photos(self):
        self.assertEqual(self.message.photos, "")

    def test_parse_share(self):
        self.assertEqual(self.message.share, "")

    def test_parse_type(self):
        self.assertEqual(self.message.type, "Generic")

    def test_get_datetime(self):
        datetime = '2018-08-25 16:22:29'
        self.assertEqual(datetime, self.message.get_datetime())


if __name__ == '__main__':
    unittest.main()
