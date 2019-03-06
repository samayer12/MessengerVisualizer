import unittest
from Message import Message
from FileIO import FileIO

skeleton_JSON = FileIO()
skeleton_JSON.open_file('Messages\message_skeleton.json')
message = Message(skeleton_JSON.data)


class MessageTest(unittest.TestCase):
    def parse_sender(self):
        self.assertEqual(message.sender_name, "Alice")

    def parse_timestamp(self):
        self.assertEqual(message.timestamp_ms, 1535232149475)

    def parse_content(self):
        self.assertEqual(message.content, "Hello, Bob")

    def parse_photos(self):
        self.assertEqual(message.photos, "")

    def parse_share(self):
        self.assertEqual(message.share, "")

    def parse_type(self):
        self.assertEqual(message.type, "Generic")

