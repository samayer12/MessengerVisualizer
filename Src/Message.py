import datetime


class Message:

    sender_name = ''
    timestamp_ms = ''
    content = ''
    type = ''

    def __init__(self, message_source):
        self.sender_name = message_source["sender_name"]
        self.timestamp_ms = message_source["timestamp_ms"]
        self.content = message_source["content"]
        self.type = message_source["type"]