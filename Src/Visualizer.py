import sys, getopt, os, nltk
from FileIO import FileIO
from Conversation import Conversation


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
    inputfile = ''
    outputdir = ''
    wordlist = ''

    try:
        opts, args = getopt.getopt(argv, "f:w:oh", ["ffile=", "odir=", "wlist="])
    except getopt.GetoptError:
        print('Error, check file paths and run with these options:\n'
              'Visualizer.py -f <inputfile> [-o <outputfile>] [-w <wordlist>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Visualizer.py -f <inputfile> [-o <outputfile>] [-w <wordlist>]')
            sys.exit()
        elif opt in ("-f", "--ifile"):
            inputfile = arg
        elif opt in ("-w", "--wordlist"):
            wordlist = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg

    fileIO = FileIO()
    conversation = Conversation(fileIO.open_json(inputfile))

    count_word_frequency(conversation.get_text(), fileIO.open_text(wordlist))

    print(conversation.get_messages())
    print(conversation.get_messages_by_sender())


if __name__ == "__main__":
    main(sys.argv[1:])

print("End")
