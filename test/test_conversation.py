import unittest, json, datetime
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
        cls.skeleton_JSON = None
        cls.conversation = None

    def test_parse_participants(self):
        self.assertEqual(self.conversation.participants, ['Alice', 'Bob'])

    def test_parse_messages(self):
        for msg in self.conversation.messages:
            # Kludge because I store timestamps as datetime, please forgive me
            msg.timestamp = int(msg.timestamp.timestamp() * 1000 - 18000000)
        filtered_messages = del_none(self.conversation.messages)

        messages_list = json.dumps(filtered_messages, default=lambda m: m.__dict__)
        messages_list = messages_list.replace("\"", "\'")
        messages_list = messages_list.replace("timestamp", "timestamp_ms")

        self.maxDiff = None
        self.assertEqual(messages_list, str((self.skeleton_JSON.data["messages"])))

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
        cls.skeleton_JSON = None
        cls.conversation = None

    def test_count_messages(self):
        totals = self.conversation.get_message_totals()

        self.assertEqual(totals["Alice"], 4)
        self.assertEqual(totals["Bob"], 3)

    def test_count_photos(self):
        totals = self.conversation.get_photo_totals()

        self.assertEqual(totals["Alice"], 1)
        self.assertNotIn("Bob", totals)

    def test_count_shares(self):
        totals = self.conversation.get_share_totals()

        self.assertNotIn("Alice", totals)
        self.assertEqual(totals["Bob"], 1)

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
        avg_message = self.conversation.get_average_message_length(self.conversation.get_text())
        self.assertEqual(avg_message, 4.5)

    def test_prepare_all_messages(self):
        raw_text = self.conversation.get_messages()

        self.assertEqual(raw_text,
                         u"2019-08-24 02:32:23: Alice: Hello, Bob\n"
                         u"2019-08-26 14:22:29: Bob: Hello, Alice.\n"
                         u"2019-08-29 09:22:29: Alice: How are you?\n"
                         u"2019-08-30 09:22:29: Bob: I am well, thank you.\n"
                         u"2019-09-01 09:22:29: Alice: I am glad to hear that.\n"
                         )

    def test_get_messages_by_sender(self):
        raw_text = self.conversation.get_messages_by_sender()

        self.assertEqual(raw_text,
                         {"Alice": u"2019-08-24 02:32:23: Hello, Bob\n2019-08-29 09:22:29: How are you?\n"
                                   u"2019-09-01 09:22:29: I am glad to hear that.\n",
                          "Bob": u"2019-08-26 14:22:29: Hello, Alice.\n2019-08-30 09:22:29: I am well, thank you.\n"}
                         )

    def test_get_message_count_by_type(self):
        message_types = self.conversation.get_type_count()

        self.assertEqual(message_types,
                         {"Content": 5,
                          "Photos": 1,
                          "Share": 1}
                          )

    def test_get_message_count_by_day(self):
        message_counts = self.conversation.get_by_day()

        self.assertEqual(message_counts,
                         {"Monday": 1,
                          "Tuesday": 1,
                          "Wednesday": 1,
                          "Thursday": 1,
                          "Friday": 1,
                          "Saturday": 1,
                          "Sunday": 1})

    def test_get_message_count_by_hour(self):
        message_counts = self.conversation.get_by_hour()

        self.assertEqual(message_counts,
                         [(0, 0), (1, 0), (2, 1), (3, 0), (4, 0), (5, 0),
                          (6, 0), (7, 0), (8, 0), (9, 5), (10, 0), (11, 0),
                          (12, 0), (13, 0), (14, 1), (15, 0), (16, 0), (17, 0),
                          (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0)])

    def test_get_message_count_by_type_for_single_participant(self):
        pass