import logging
from typing import Any, Union, List

import nltk
import matplotlib.pyplot as plt
import numpy as np

visualizer_logger = logging.getLogger('MessengerViz.visualizer')

def strip_common(words: list[str], wordlist: list[str]) -> list[str]:
    """
    Create the set difference from two lists of strings
    :param words: The "source" that may have undesired entries
    :param wordlist: List of words to remove from `words`
    :return: words - wordlist
    """
    visualizer_logger.debug("Filtering %d words from dataset.", len(wordlist))
    return [word.lower() for word in words if word.lower() not in wordlist]


def plot_frequency(filepath: str, title: str, x_label: str, y_label: str, data: Any) -> None:
    """
    Wrapper function to matplotlib.bar to abstract away some formatting commands
    :param filepath: Output to save file
    :param title: Label to display at top of chart
    :param x_label: Label for x-axis
    :param y_label: Label for y-axis
    :param data: Source data to graph, typically one of the "get" methods in Conversation.py
    :return:
    """
    plt.bar(*zip(*data.items()))
    plt.xticks(np.arange(len(data.keys())), data.keys(), rotation=45)
    plt.title(title)
    plt.ylabel(x_label)
    plt.xlabel(y_label)
    visualizer_logger.debug('Saving frequency chart to: %s', filepath)
    plt.savefig(filepath)
    plt.show()


def plot_message_type_balance(filepath: str, sender: str, data: List[str], label: List[str]) -> None:
    """
    Wrapper function to matplotlib.pytplot.pie to abstract away some formatting commands
    :param filepath: Output to save file
    :param sender: Name of sender in conversation
    :param data: Message data
    :param label: Label to display at top of chart
    :return: None
    """
    plt.pie(data, labels=label)
    plt.title("Message Balance for " + sender)
    visualizer_logger.debug('Saving message balance chart to: %s', filepath)
    plt.savefig(filepath)
    plt.show()


def plot_word_frequency(filepath: str, conversation: str, wordlist: Union[list[str], None] = None) -> None:
    """
    Wrapper function to nltk.FreqDist to abstract away some formatting commands
    :param filepath: Output to save file
    :param conversation: Conversation data
    :param wordlist: List of words to remove from Frequency Distribution
    :return:
    """
    tokens = conversation.split()
    if wordlist is not None:
        tokens = strip_common(tokens, wordlist)
    figure = plt.figure(figsize=(16, 6))

    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ":" + str(val))

    freq.plot(50, cumulative=False, title="Word Frequency Across Data Set")
    visualizer_logger.debug('Saving word frequency chart to: %s', filepath)
    figure.savefig(filepath, bbox_inches="tight")
