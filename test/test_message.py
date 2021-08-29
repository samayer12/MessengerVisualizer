import unittest
from src.FileIO import FileIO
from src.Message import Message


class MessageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.skeleton_JSON = FileIO()
        cls.skeleton_JSON.open_json("test/Messages/message_skeleton_text.json")
        cls.message = Message(cls.skeleton_JSON.data)

    @classmethod
    def tearDownClass(cls):
        del cls.skeleton_JSON
        del cls.message

    def test_parse_sender(self):
        self.assertEqual(self.message.sender_name, "Alice")

    def test_parse_timestamp(self):
        self.assertEqual(1535232149.475, self.message.timestamp.timestamp())

    def test_parse_content(self):
        self.assertEqual(self.message.content, "Hello, Bob")

    def test_parse_photos(self):
        self.assertEqual(self.message.photos, "")

    def test_parse_share(self):
        self.assertEqual(self.message.share, "")

    def test_parse_type(self):
        self.assertEqual(self.message.type, "Generic")

    def test_get_datetime(self):
        datetime = "2018-08-25 16:22:29"
        self.assertEqual(datetime, self.message.get_datetime())

    def test_format_chatlog(self):
        expected = u"2018-08-25 16:22:29: Alice: Hello, Bob\n"
        self.assertEqual(expected, self.message.format_chatlog())



class ReactionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.skeleton_JSON = FileIO()
        cls.skeleton_JSON.open_json("test/Messages/message_skeleton_reaction.json")
        cls.message = Message(cls.skeleton_JSON.data)

    @classmethod
    def tearDownClass(cls):
        del cls.skeleton_JSON
        del cls.message

    def test_parse_like_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Like"])

    def test_parse_dislike_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Dislike"])

    def test_parse_angry_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Angry"])

    def test_parse_sad_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Sad"])

    def test_parse_wow_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Wow"])

    def test_parse_laughing_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Funny"])

    def test_parse_love_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Love"])

    def test_parse_unsupported_reaction(self):
        self.assertEqual(1, self.message.reactions.get("Alice")["Unsupported"])
        self.assertEqual(["\u0078\u006b\u0063\u0064"], self.message.unsupported_reactions)

    def test_assign_reaction_owner(self):
        from collections import defaultdict

        expected_alice = defaultdict(
            int, {"Dislike": 1, "Like": 1, "Angry": 1, "Sad": 1, "Wow": 1, "Funny": 1, "Love": 1, "Unsupported": 1}
        )
        expected_bob = None

        self.assertEqual(expected_alice, self.message.reactions.get("Alice"))
        self.assertEqual(expected_bob, self.message.reactions.get("Bob"))


if __name__ == "__main__":
    unittest.main()
