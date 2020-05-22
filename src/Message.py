import datetime
from collections import defaultdict


def parse_reactions(reactions):
    message_reactions = defaultdict(lambda: defaultdict(int))
    unsupported_reactions = []
    if reactions is None:
        raise KeyError
    for react in reactions:
        current_reaction = react['reaction']
        current_actor = react['actor']
        if current_reaction == "\u00f0\u009f\u0091\u008e":
            message_reactions[current_actor]['Dislike'] += 1
        elif current_reaction == "\u00f0\u009f\u0091\u008d":
            message_reactions[current_actor]['Like'] += 1
        elif current_reaction == "\u00f0\u009f\u0098\u00a0":
            message_reactions[current_actor]['Angry'] += 1
        elif current_reaction == "\u00f0\u009f\u0098\u00a2":
            message_reactions[current_actor]['Sad'] += 1
        elif current_reaction == "\u00f0\u009f\u0098\u00ae":
            message_reactions[current_actor]['Wow'] += 1
        elif current_reaction == "\u00f0\u009f\u0098\u0086":
            message_reactions[current_actor]['Funny'] += 1
        elif current_reaction == "\u00f0\u00e2\u009d\u00a4":
            message_reactions[current_actor]['Love'] += 1
        else:
            message_reactions[current_actor]['Unsupported'] += 1
            unsupported_reactions.append(current_reaction)

    return message_reactions, unsupported_reactions


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
            self.reactions, self.unsupported_reactions = parse_reactions(message_source['reactions'])
        except KeyError:
            # There's no reaction, so why bother?
            pass

    def get_datetime(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
