import datetime


class Message:

    sender = ""
    timestamp = ""
    content = ""
    type = ""

    def __init__(self, message_source):
        self.sender = message_source["sender_name"]
        self.timestamp = message_source["timestamp_ms"]
        self.content = message_source["content"]
        self.type = message_source["type"]