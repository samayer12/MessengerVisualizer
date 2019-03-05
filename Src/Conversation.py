import json
from Message import Message


class Conversation:
    participants = ""
    messages = []
    title = ""
    is_still_participant = False
    thread_type = ""
    thread_path = ""

    def __init__(self, conversation_source):
        self.participants = conversation_source["participants"]
        for msg in conversation_source["messages"]:
            self.messages.append(Message(msg))
        self.title = conversation_source["title"]
        self.is_still_participant = conversation_source["is_still_participant"]
        self.thread_type = conversation_source["thread_type"]
        self.thread_path = conversation_source["thread_path"]
