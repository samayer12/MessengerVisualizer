import unittest

from FileIO import FileIO
from Message import Message

skeleton_JSON = FileIO()
skeleton_JSON.open_file('Messages\message_skeleton.json')
message = Message(skeleton_JSON.data)


class MessageTest(unittest.TestCase):
    def test_parse_sender(self):
        self.assertEqual(message.sender_name, "Alice")

    def test_parse_timestamp(self):
        self.assertEqual(message.timestamp_ms, 1535232149475)

    def test_parse_content(self):
        self.assertEqual(message.content, "Hello, Bob")

    def test_parse_photos(self):
        self.assertEqual(message.photos, "")

    def test_parse_share(self):
        self.assertEqual(message.share, "")

    def test_parse_type(self):
        self.assertEqual(message.type, "Generic")

