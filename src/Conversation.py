from collections import Counter
from itertools import chain
from typing import Dict, Any

from src.Message import Message
from nltk import sent_tokenize, word_tokenize
from string import punctuation


class Conversation:

    def __init__(self, conversation_source: Dict[str, Any]) -> None:
        self.participants = []
        for p in conversation_source["participants"]:
            self.participants.append(p.get("name", "ParseError"))
        self.messages = []
        for msg in conversation_source["messages"]:
            self.messages.append(Message(msg))
        self.reactions = {}
        for msg in self.messages:
            try:
                self.reactions.update(msg.reactions)
            except:
                # No reaction in that message
                pass
        self.title = conversation_source["title"]
        self.is_still_participant = conversation_source["is_still_participant"]
        self.thread_type = conversation_source["thread_type"]
        self.thread_path = conversation_source["thread_path"]
        self.message_count_by_sender = {}

    def get_message_totals(self) -> Dict:
        counter = Counter(msg.sender_name for msg in self.messages)

        return dict(counter)

    def get_text_totals(self) -> Dict:
        text_messages = [msg for msg in self.messages if msg.content != ""]

        counter = Counter(msg.sender_name for msg in text_messages)

        return dict(counter)

    def get_photo_totals(self) -> Dict:
        photo_messages = [msg for msg in self.messages if msg.photos != ""]

        counter = Counter(msg.sender_name for msg in photo_messages)

        return dict(counter)

    def get_share_totals(self) -> Dict:
        share_messages = [msg for msg in self.messages if msg.share != ""]

        counter = Counter(msg.sender_name for msg in share_messages)

        return dict(counter)

    def get_text(self) -> str:
        raw_messages = ""
        raw_messages = raw_messages.join([(msg.content + "\n") for msg in self.messages if msg.content != ""])
        return raw_messages

    def get_messages(self) -> str:
        raw_messages = ""
        raw_messages = raw_messages.join([(msg.get_datetime() + ": " + msg.sender_name + ": " + msg.content + "\n")
                                          for msg in self.messages if msg.content != ""])
        return raw_messages

    def get_messages_by_sender(self) -> Dict[str, str]:
        messages_by_sender = {}

        for p in self.participants:
            raw_messages = ""
            raw_messages = raw_messages.join([(msg.get_datetime() + ": " + msg.content + "\n")
                                              for msg in self.messages if (msg.content != "" and msg.sender_name == p)])
            messages_by_sender[p] = raw_messages

        return messages_by_sender

    def get_message_type_count(self) -> Dict[str, Dict[str, int]]:
        message_type_dict = {}
        for p in self.participants:
            message_type_dict[p] = {"Content": 0, "Photos": 0, "Share": 0}

        for msg in self.messages:
            if msg.content != "":
                message_type_dict[msg.sender_name]["Content"] += 1
            if msg.photos != "":
                message_type_dict[msg.sender_name]["Photos"] += 1
            if msg.share != "":
                message_type_dict[msg.sender_name]["Share"] += 1

        def append_global_totals(input_dict: Dict) -> Dict[str, Dict[str, int]]:
            global_message_types = {"Global": {"Content": 0, "Photos": 0, "Share": 0}}
            for participant in input_dict:
                for key, value in input_dict[participant].items():
                    global_message_types["Global"][key] += value
            return dict(chain(input_dict.items(), global_message_types.items()))

        message_type_dict = append_global_totals(message_type_dict)
        return message_type_dict

    def get_by_day(self) -> Dict[str, int]:
        days = dict.fromkeys(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 0)
        for msg in self.messages:
            days[(msg.timestamp.strftime("%A"))] += 1
        return days

    def get_by_hour(self) -> Dict[int, int]:
        hours = dict.fromkeys(range(24), 0)
        for msg in self.messages:
            hours[int((msg.timestamp.strftime("%H")))] += 1
        return dict(sorted(hours.items()))

    def get_average_message_length(self) -> float:
        words = word_tokenize(self.get_text())
        words = [''.join(char for char in strings if char not in punctuation) for strings in words]
        words = [string for string in words if string]
        return len(words)/len(sent_tokenize(self.get_text()))

    def get_reaction_counts(self) -> Dict:
        return self.reactions

