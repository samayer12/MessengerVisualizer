import unittest
from Conversation import Conversation
from FileIO import FileIO

skeleton_JSON = FileIO()
skeleton_JSON.open_file('Messages\conversation_skeleton.json')
conversation = Conversation(skeleton_JSON.data)


class ConversationTest(unittest.TestCase):
    def parse_participants(self):
        self.assertEqual(conversation.participants, [{'name': 'Alice'}, {'name': 'Bob'}])

    def parse_messages(self):
        self.assertEqual(conversation.messages, [
            {
              "sender_name": "Alice",
              "timestamp_ms": 1535232149475,
              "content": "Hello, Bob",
              "type": "Generic"
            },
            {
              "sender_name": "Bob",
              "timestamp_ms": 1535228809355,
              "content": "Hello, Alice.",
              "type": "Generic"
            }
          ])

    def parse_title(self):
        self.assertEqual(conversation.title, "Conversation")

    def parse_is_still_participant(self):
        self.assertEqual(conversation.is_still_participant, True)

    def parse_thread_type(self):
        self.assertEqual(conversation.thread_type, 'Regular')

    def parse_thread_path(self):
        self.assertEqual(conversation.thread_path, "Conversation_1337")
