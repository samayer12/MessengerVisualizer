import datetime


class Message:

    sender_name = ''
    timestamp = ''
    content = None
    photos = None
    share = None
    type = ''

    def __init__(self, message_source):
        self.sender_name = message_source["sender_name"]
        self.timestamp = datetime.datetime.fromtimestamp(message_source["timestamp_ms"] / 1000)
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

    def get_datetime(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')