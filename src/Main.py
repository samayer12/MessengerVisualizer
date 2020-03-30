import sys
import getopt
import argparse
from src.FileIO import FileIO
from src.Conversation import Conversation
from src.Visualizer import Visualizer


def graphData(conversationData, wordlist):
    Visualizer.plot_frequency(conversationData.get_by_hour())
    Visualizer.plot_frequency(conversationData.get_by_day())
    Visualizer.plot_word_frequency(conversationData.get_text(), wordlist)

    message_types_by_sender = conversationData.get_message_type_count()
    for sender in message_types_by_sender:
        Visualizer.plot_message_type_balance(list(message_types_by_sender[sender].values()),
                                             list(message_types_by_sender[sender].keys()))


def printMessages(conversationData):
    print(conversationData.get_messages())
    print(conversationData.get_messages_by_sender())
    print(conversationData.get_by_day())


def main(argv):
    parser = argparse.ArgumentParser(description='Visualize FB messenger data from .json files')
    parser.add_argument('-i', '--inputfile', metavar='InFile', dest='inputfile', required=True,
                        nargs=1, help='.json file containing messenger data')
    parser.add_argument('-o', '--outputdirectory', metavar='OutFile', dest='outputdir', default=None, required=False,
                        nargs=1, help='Directory to put visualizations')
    parser.add_argument('-w', '--wordlist', metavar='Wordlist', dest='wordlist', default=None, required=False,
                        nargs=1, help='.txt file of words to ignore')

    try:
        args = parser.parse_args()
        fileIO = FileIO()
        visualizer = Visualizer()
        inputfile = args.inputfile[0]
        conversation = Conversation(fileIO.open_json(inputfile))
        outputdir = args.outputdir
        try:
            wordlist = fileIO.open_text(args.wordlist[0])
        except TypeError:
            wordlist = None
            print("Wordlist not defined. Moving on.")

        graphData(conversation, wordlist)
        printMessages(conversation)


    except getopt.GetoptError:
        print('\nERROR: Check file paths\n')
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
