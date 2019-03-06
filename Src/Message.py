import datetime


class Message:

    sender_name = ''
    timestamp_ms = ''
    content = None
    photos = None
    share = None
    type = ''

    def __init__(self, message_source):
        self.sender_name = message_source["sender_name"]
        self.timestamp_ms = message_source["timestamp_ms"]
        try:
            self.content = message_source["content"]
        except KeyError:
            self.content = ""
            pass
        try:
            self.photos = message_source["photos"]
        except KeyError:
            self.photos = ""
            pass
        try:
            self.share = message_source["share"]
        except KeyError:
            self.share = ""
            pass
        self.type = message_source["type"]