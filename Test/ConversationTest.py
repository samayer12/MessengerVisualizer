import unittest, json
from Conversation import Conversation
from FileIO import FileIO

skeleton_JSON = FileIO()
skeleton_JSON.open_file('Messages\conversation_skeleton.json')
conversation = Conversation(skeleton_JSON.data)


class InitializationTest(unittest.TestCase):
    def parse_participants(self):
        self.assertEqual(conversation.participants, ['Alice', 'Bob'])

    def parse_messages(self):
        messages_list = json.dumps(conversation.messages, default=lambda m: m.__dict__)
        messages_list = messages_list.replace("\"", "\'")

        self.assertEqual(messages_list, str((skeleton_JSON.data["messages"])))

    def parse_title(self):
        self.assertEqual(conversation.title, "Conversation")

    def parse_is_still_participant(self):
        self.assertEqual(conversation.is_still_participant, True)

    def parse_thread_type(self):
        self.assertEqual(conversation.thread_type, 'Regular')

    def parse_thread_path(self):
        self.assertEqual(conversation.thread_path, "Conversation_1337")


class ProcessingTest(unittest.TestCase):
    def creates_message_counts(self):

        totals = conversation.get_message_totals()

        self.assertEqual(totals["Alice"], 1)
        self.assertEqual(totals["Bob"], 1)
