import unittest

from src.FileIO import FileIO
from src.Message import Message

skeleton_JSON = FileIO()
skeleton_JSON.open_json('Messages/message_skeleton.json')
message = Message(skeleton_JSON.data)


class MessageTest(unittest.TestCase):
    def test_parse_sender(self):
        self.assertEqual(message.sender_name, "Alice")

    def test_parse_timestamp(self):
        self.assertEqual(message.timestamp.timestamp() *1000 - 18000000, 1535232149475)

    def test_parse_content(self):
        self.assertEqual(message.content, "Hello, Bob")

    def test_parse_photos(self):
        self.assertEqual(message.photos, "")

    def test_parse_share(self):
        self.assertEqual(message.share, "")

    def test_parse_type(self):
        self.assertEqual(message.type, "Generic")

    def test_get_datetime(self):
        datetime = '2018-08-25 21:22:29'
        self.assertEqual(datetime, message.get_datetime())

