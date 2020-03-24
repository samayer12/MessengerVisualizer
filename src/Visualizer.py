import nltk
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self):
        pass

    @staticmethod
    def strip_common(words, wordlist):
        return [word.lower() for word in words if word.lower() not in wordlist]

    @staticmethod
    def plot_frequency(data):
        plt.bar(*zip(*data.items()))
        plt.xticks(rotation=45)
        plt.show()

    @staticmethod
    def plot_message_type_balance(data, label):
        plt.pie(data, labels=label)
        plt.show()

    def plot_word_frequency(self, conversation, wordlist=None):
        tokens = [t for t in conversation.split()]
        if wordlist is not None:
            tokens = self.strip_common(tokens, wordlist)
        freq = nltk.FreqDist(tokens)
        for key, val in freq.items():
            print(str(key) + ':' + str(val))

        return freq.plot(50, cumulative=False)
