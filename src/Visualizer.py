import sys
import getopt
import nltk
import argparse
from src.FileIO import FileIO
from src.Conversation import Conversation


def strip_common(words, wordlist):
    return [word for word in words if word not in wordlist]


def count_word_frequency(conversation, wordlist):
    tokens = [t for t in conversation.split()]
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
        inputfile = args.inputfile[0]
        outputdir = args.outputdir
        wordlist = args.wordlist[0]
        fileIO = FileIO()
        conversation = Conversation(fileIO.open_json(inputfile))

        count_word_frequency(conversation.get_text(), fileIO.open_text(wordlist))

        print(conversation.get_messages())
        print(conversation.get_messages_by_sender())
    except getopt.GetoptError:
        print('\nERROR: Check file paths\n')
        parser.print_help()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

print("End")
