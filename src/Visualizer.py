from typing import Any, Union

import nltk
import matplotlib.pyplot as plt
import numpy as np


def strip_common(words: list[str], wordlist: list[str]) -> list[str]:
    """
    Create the set difference from two lists of strings
    :param words: The "source" that may have undesired entries
    :param wordlist: List of words to remove from `words`
    :return: words - wordlist
    """
    return [word.lower() for word in words if word.lower() not in wordlist]


def plot_frequency(filepath: str, title: str, x_label: str, y_label: str, data: Any) -> None:
    plt.bar(*zip(*data.items()))
    plt.xticks(np.arange(len(data.keys())), data.keys(), rotation=45)
    plt.title(title)
    plt.ylabel(x_label)
    plt.xlabel(y_label)
    plt.savefig(filepath)
    plt.show()


def plot_message_type_balance(filepath: str, sender: str, data: Any, label: str) -> None:
    plt.pie(data, labels=label)
    plt.title("Message Balance for " + sender)
    plt.savefig(filepath)
    plt.show()


def plot_word_frequency(filepath: str, conversation: str, wordlist: Union[list[str], None] = None) -> None:
    tokens = conversation.split()
    if wordlist is not None:
        tokens = strip_common(tokens, wordlist)
    figure = plt.figure(figsize=(16, 6))

    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ":" + str(val))

    freq.plot(50, cumulative=False, title="Word Frequency Across Data Set")
    figure.savefig(filepath, bbox_inches="tight")
