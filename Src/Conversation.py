import datetime
from collections import Counter

from Message import Message


class Conversation:
    participants = []
    messages = []
    title = ""
    is_still_participant = False
    thread_type = ""
    thread_path = ""
    message_count_by_sender = {}

    def __init__(self, conversation_source):
        for p in conversation_source["participants"]:
            self.participants.append(p["name"])
        for msg in conversation_source["messages"]:
            self.messages.append(Message(msg))
        self.title = conversation_source["title"]
        self.is_still_participant = conversation_source["is_still_participant"]
        self.thread_type = conversation_source["thread_type"]
        self.thread_path = conversation_source["thread_path"]

    def get_message_totals(self):
        counter = Counter(msg.sender_name for msg in self.messages)

        return dict(counter)

    def get_photo_totals(self):
        photo_messages = [msg for msg in self.messages if msg.photos != ""]

        counter = Counter(msg.sender_name for msg in photo_messages)

        return dict(counter)

    def get_share_totals(self):
        share_messages = [msg for msg in self.messages if msg.share != ""]

        counter = Counter(msg.sender_name for msg in share_messages)

        return dict(counter)

    def get_text(self):
        raw_messages = ""
        raw_messages = raw_messages.join([(msg.content + "\n") for msg in self.messages if msg.content != ""])
        return raw_messages

    def get_messages(self):
        raw_messages = ""
        raw_messages = raw_messages.join([(msg.get_datetime() + ": " + msg.sender_name + ": " + msg.content + "\n")
                                          for msg in self.messages if msg.content != ""])
        return raw_messages

    def get_messages_by_sender(self):
        messages_by_sender = {}

        for p in self.participants:
            raw_messages = ""
            raw_messages = raw_messages.join([(msg.get_datetime() + " : " + msg.content + "\n")
                                              for msg in self.messages if (msg.content != "" and msg.sender_name == p)])
            messages_by_sender[p] = raw_messages

        return messages_by_sender

    def get_type_count(self):
        messages_by_type = {"Content":0, "Photos": 0, "Share": 0}

        for msg in self.messages:
            if msg.content != "":
                messages_by_type["Content"] += 1
            if msg.photos != "":
                messages_by_type["Photos"] += 1
            if msg.share != "":
                messages_by_type["Share"] += 1

        return messages_by_type

        pass

    def get_by_day(self):

        days = []
        for msg in self.messages:
            days.append((msg.timestamp.strftime("%A")))
        return Counter(days)
