import datetime
import logging
from collections import defaultdict
from typing import Dict, Any

message_logger = logging.getLogger('MessengerViz.message')


def parse_reactions(reactions: Dict[str, Dict[str, str]]) -> tuple[defaultdict[Any, defaultdict[Any, int]], list[str]]:
    """
    Process a message and return any reactions that were applied by one or more actors in the conversation.

    :param reactions: Dictionary of reaction(s) to a message
    :return: Tuple of reaction counts and a list of any unsupported reactions, if encountered
    """
    message_reactions = defaultdict(lambda: defaultdict(int))
    unsupported_reactions = []
    if reactions is None:
        raise KeyError

    known_reactions = {"\u00f0\u009f\u0091\u008e": "Dislike",
                       "\u00f0\u009f\u0091\u008d": "Like",
                       "\u00f0\u009f\u0098\u00a0": "Angry",
                       "\u00f0\u009f\u0098\u00a2": "Sad",
                       "\u00f0\u009f\u0098\u00ae": "Wow",
                       "\u00f0\u009f\u0098\u0086": "Funny",
                       "\u00f0\u00e2\u009d\u00a4": "Love"}

    for react in reactions:
        current_reaction = react["reaction"]
        current_actor = react["actor"]
        if current_reaction in known_reactions.keys():
            message_reactions[current_actor][known_reactions[current_reaction]] += 1
        else:
            message_reactions[current_actor]["Unsupported"] += 1
            unsupported_reactions.append(current_reaction)

    return message_reactions, unsupported_reactions


class Message:
    def __init__(self, message_source: Dict[str, Any]) -> None:
        """
        Represent a Facebook Messenger Message and key attributes about the message.

        :param message_source: Dict containing message data
        """
        self.logger = logging.getLogger('MessengerViz.message.Message')
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
            self.reactions, self.unsupported_reactions = parse_reactions(message_source["reactions"])
            if self.unsupported_reactions:
                self.logger.info('Received unsupported reactions: %s', self.unsupported_reactions)
        except KeyError:
            # No reaction, so why bother?
            pass

    def get_datetime(self) -> str:
        """
        :return: A standard datetime string for the context of the project.
        """
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def format_chatlog(self) -> str:
        """
        :return: A standard chatlog string for the context of the project.
        """
        return f"{self.get_datetime()}: {self.sender_name}: {self.content}\n"

    def format_csv(self) -> str:
        """
        :return: A standard chatlog message ready for .csv processing as a table
        """
        return f"{self.get_datetime().replace(' ',',').replace(':', ',')},{self.sender_name},\"{self.content}\"\n"
