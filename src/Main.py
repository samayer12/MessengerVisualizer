import sys
import getopt
import argparse
from src.FileIO import FileIO
from src.Conversation import Conversation
from src.Visualizer import Visualizer


def graphData(conversationData):
    Visualizer.plot_frequency(conversationData)
    Visualizer.plot_frequency(conversationData)
    #Visualizer.plot_word_frequency(conversationData)

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
        visualizer = Visualizer()
        inputfile = args.inputfile[0]
        conversation = Conversation(fileIO.open_json(inputfile))

        if args.outputdir:
            outputdir = args.outputdir
        if args.wordlist:
            wordlist = args.wordlist[0]
            words = fileIO.open_text(wordlist)
            visualizer.plot_word_frequency(conversation.get_text(), words)
        else:
            pass
            visualizer.plot_word_frequency(conversation.get_text())


        message_types_by_sender = conversation.get_message_type_count()
        for sender in message_types_by_sender:
            visualizer.plot_message_type_balance(list(message_types_by_sender[sender].values()),
                                                 list(message_types_by_sender[sender].keys()))

        print(conversation.get_messages())
        print(conversation.get_messages_by_sender())
        print(conversation.get_by_day())

    except getopt.GetoptError:
        print('\nERROR: Check file paths\n')
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])

print("End")
