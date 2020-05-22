import datetime
from collections import defaultdict

class Message:

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
        try:
            self.reactions, self.unsupported_reactions = self.parse_reactions(message_source['reactions'])
        except KeyError:
            # There's no reaction, so why bother?
            pass

    def parse_reactions(self, reactions):
        message_reactions = defaultdict(int)
        unsupported_reactions = []
        if reactions is None:
            raise KeyError
        for react in reactions:
            current_reaction = react['reaction']
            if current_reaction == "\u00f0\u009f\u0091\u008e":
                message_reactions['Dislike'] += 1
            elif current_reaction == "\u00f0\u009f\u0091\u008d":
                message_reactions['Like'] += 1
            elif current_reaction == "\u00f0\u009f\u0098\u00a0":
                message_reactions['Angry'] += 1
            elif current_reaction == "\u00f0\u009f\u0098\u00a2":
                message_reactions['Sad'] += 1
            elif current_reaction == "\u00f0\u009f\u0098\u00ae":
                message_reactions['Wow'] += 1
            elif current_reaction == "\u00f0\u009f\u0098\u0086":
                message_reactions['Funny'] += 1
            elif current_reaction == "\u00f0\u00e2\u009d\u00a4":
                message_reactions['Love'] += 1
            else:
                message_reactions['Unsupported'] += 1
                unsupported_reactions.append(current_reaction)

        return message_reactions, unsupported_reactions

    def get_datetime(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
