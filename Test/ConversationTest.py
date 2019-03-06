import unittest, json
from Conversation import Conversation
from FileIO import FileIO

skeleton_JSON = FileIO()
skeleton_JSON.open_file('Messages\conversation_skeleton.json')
conversation = Conversation(skeleton_JSON.data)


def del_none(data):
    for entry in data:
        data_dictionary = entry.__dict__
        for key in data_dictionary.copy():
            if data_dictionary[key] is (None or ''):
                del data_dictionary[key]
    return data


class InitializationTest(unittest.TestCase):
    def test_parse_participants(self):
        self.assertEqual(conversation.participants, ['Alice', 'Bob'])

    def test_parse_messages(self):
        filtered_messages = del_none(conversation.messages)


        messages_list = json.dumps(filtered_messages, default=lambda m: m.__dict__)
        messages_list = messages_list.replace("\"", "\'")

        self.maxDiff=None
        self.assertEqual(messages_list, str((skeleton_JSON.data["messages"])))

    def test_parse_title(self):
        self.assertEqual(conversation.title, "Conversation")

    def test_parse_is_still_participant(self):
        self.assertEqual(conversation.is_still_participant, True)

    def test_parse_thread_type(self):
        self.assertEqual(conversation.thread_type, 'Regular')

    def test_parse_thread_path(self):
        self.assertEqual(conversation.thread_path, "Conversation_1337")


class ProcessingTest(unittest.TestCase):
    def test_count_messages(self):
        totals = conversation.get_message_totals()

        self.assertEqual(totals["Alice"], 2)
        self.assertEqual(totals["Bob"], 2)

    def test_count_photos(self):
        totals = conversation.get_photo_totals()

        self.assertEqual(totals["Alice"], 1)
        self.assertNotIn("Bob", totals)

    def test_count_shares(self):
        totals = conversation.get_share_totals()

        self.assertNotIn("Alice", totals)
        self.assertEqual(totals["Bob"], 1)
