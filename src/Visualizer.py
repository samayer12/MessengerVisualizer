import sys
import getopt
import nltk
import argparse
from src.FileIO import FileIO
from src.Conversation import Conversation


def strip_common(words, wordlist):
    return [word for word in words if word not in wordlist]


def count_word_frequency(conversation, wordlist=None):
    tokens = [t for t in conversation.split()]
    if wordlist is not None:
        tokens = strip_common(tokens, wordlist)
    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))

    freq.plot(50, cumulative=False)


def main(argv):
    parser = argparse.ArgumentParser(description='Visualize FB messenger data from .json files')
    parser.add_argument('-i', '--inputfile', metavar='InFile', dest='inputfile', required=True,
                        nargs=1, help='.json file containing messenger data')
    parser.add_argument('-o', '--outputdirectory', metavar='OutFile', dest='outputdir', required=False,
                        nargs=1, help='Directory to put visualizations')
    parser.add_argument('-w', '--wordlist', metavar='Wordlist', dest='wordlist', required=False,
                        nargs=1, help='.txt file of words to ignore')

    try:
        args = parser.parse_args()
        fileIO = FileIO()

        inputfile = args.inputfile[0]
        conversation = Conversation(fileIO.open_json(inputfile))

        if args.outputdir:
            outputdir = args.outputdir
        if args.wordlist:
            wordlist = args.wordlist[0]
            words = fileIO.open_text(wordlist)
            count_word_frequency(conversation.get_text(), words)
        else:
            count_word_frequency(conversation.get_text())

        print(conversation.get_messages())
        print(conversation.get_messages_by_sender())
    except getopt.GetoptError:
        print('\nERROR: Check file paths\n')
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])

print("End")
