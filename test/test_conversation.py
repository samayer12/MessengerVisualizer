import unittest
import json
from collections import Counter
from src.Conversation import Conversation
from src.FileIO import FileIO


def del_none(data):
    for entry in data:
        data_dictionary = entry.__dict__
        for key in data_dictionary.copy():
            if data_dictionary[key] is (None or ''):
                del data_dictionary[key]
    return data


class InitializationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skeleton_JSON = FileIO()
        cls.skeleton_JSON.open_json('Messages/conversation_skeleton.json')
        cls.conversation = Conversation(cls.skeleton_JSON.data)

    @classmethod
    def tearDownClass(cls):
        del cls.skeleton_JSON
        del cls.conversation

    def test_parse_participants(self):
        self.assertEqual(['Alice', 'Bob'], self.conversation.participants)

    def test_parse_messages(self):
        for msg in self.conversation.messages:
            # Convert to epoch time to ensure data is the same as source
            msg.timestamp = int(msg.timestamp.timestamp() * 1000)
        filtered_messages = del_none(self.conversation.messages)

        messages_list = json.dumps(filtered_messages, default=lambda m: m.__dict__)
        messages_list = messages_list.replace("\"", "\'")
        messages_list = messages_list.replace("timestamp", "timestamp_ms")

        self.assertEqual(str((self.skeleton_JSON.data["messages"])), messages_list)

    def test_parse_title(self):
        self.assertEqual(self.conversation.title, "Conversation")

    def test_parse_is_still_participant(self):
        self.assertEqual(self.conversation.is_still_participant, True)

    def test_parse_thread_type(self):
        self.assertEqual(self.conversation.thread_type, 'Regular')

    def test_parse_thread_path(self):
        self.assertEqual(self.conversation.thread_path, "Conversation_1337")


class ProcessingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.skeleton_JSON = FileIO()
        cls.skeleton_JSON.open_json('Messages/conversation_skeleton.json')
        cls.conversation = Conversation(cls.skeleton_JSON.data)

    @classmethod
    def tearDownClass(cls):
        del cls.skeleton_JSON
        del cls.conversation

    def test_count_messages(self):
        totals = self.conversation.get_message_totals()

        self.assertEqual(4, totals["Alice"])
        self.assertEqual(3, totals["Bob"])

    def test_count_text_messages(self):
        totals = self.conversation.get_text_totals()

        self.assertEqual(3, totals["Alice"])
        self.assertEqual(2, totals["Bob"])

    def test_count_photos(self):
        totals = self.conversation.get_photo_totals()

        self.assertEqual(1, totals["Alice"])
        self.assertNotIn("Bob", totals)

    def test_count_shares(self):
        totals = self.conversation.get_share_totals()

        self.assertNotIn("Alice", totals)
        self.assertEqual(1, totals["Bob"])

    def test_get_text(self):
        raw_text = self.conversation.get_text()

        self.assertEqual(raw_text,
                         u"Hello, Bob\n"
                         u"Hello, Alice.\n"
                         u"How are you?\n"
                         u"I am well, thank you.\n"
                         u"I am glad to hear that.\n"
                         )

    def test_get_average_message_length(self):
        avg_message = self.conversation.get_average_message_length()
        self.assertEqual(4.5, avg_message)

    def test_prepare_all_messages(self):
        raw_text = self.conversation.get_messages()

        self.assertEqual(u"2019-08-23 21:32:23: Alice: Hello, Bob\n"
                         u"2019-08-26 09:22:29: Bob: Hello, Alice.\n"
                         u"2019-08-29 04:22:29: Alice: How are you?\n"
                         u"2019-08-30 04:22:29: Bob: I am well, thank you.\n"
                         u"2019-09-01 04:22:29: Alice: I am glad to hear that.\n",
                         raw_text
                         )

    def test_get_messages_by_sender(self):
        raw_text = self.conversation.get_messages_by_sender()

        self.assertEqual({
                             'Alice': '2019-08-23 21:32:23: Hello, Bob\n2019-08-29 04:22:29: How are you?\n2019-09-01 04:22:29: I am glad to hear that.\n',
                             'Bob': '2019-08-26 09:22:29: Hello, Alice.\n2019-08-30 04:22:29: I am well, thank you.\n'},
                         raw_text,
                         )

    def test_get_message_count_by_type(self):
        message_types = self.conversation.get_type_count()

        self.assertEqual({"Content": 5,
                          "Photos": 1,
                          "Share": 1},
                         message_types
                         )

    def test_get_message_count_by_day(self):
        message_counts = self.conversation.get_by_day()

        self.assertEqual(Counter({"Monday": 1,
                                  "Tuesday": 1,
                                  "Wednesday": 1,
                                  "Thursday": 1,
                                  "Friday": 2,
                                  "Sunday": 1}),
                         message_counts
                         )

    def test_get_message_count_by_hour(self):
        testCounter = dict.fromkeys(range(24), 0)
        testCounter[4] += 5
        testCounter[9] += 1
        testCounter[21] += 1
        message_counts = self.conversation.get_by_hour()

        self.assertEqual(dict(sorted(testCounter.items())), message_counts )

    def test_get_message_count_by_type_for_single_participant(self):
        pass


if __name__ == '__main__':
    unittest.main()
