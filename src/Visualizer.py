import nltk
import matplotlib.pyplot as plt
import numpy as np


def strip_common(words, wordlist):
    return [word.lower() for word in words if word.lower() not in wordlist]


def plot_frequency(filepath, title, x_label, y_label, data):
    plt.bar(*zip(*data.items()))
    plt.xticks(np.arange(len(data.keys())), data.keys(), rotation=45)
    plt.title(title)
    plt.ylabel(x_label)
    plt.xlabel(y_label)
    plt.savefig(filepath)
    plt.show()


def plot_message_type_balance(filepath, sender, data, label):
    plt.pie(data, labels=label)
    plt.title('Message Balance for ' + sender)
    plt.savefig(filepath)
    plt.show()


def plot_word_frequency(conversation, wordlist=None):
    tokens = [t for t in conversation.split()]
    if wordlist is not None:
        tokens = strip_common(tokens, wordlist)
    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))

    return freq.plot(50, cumulative=False, title='Word Frequency Across Data Set')
