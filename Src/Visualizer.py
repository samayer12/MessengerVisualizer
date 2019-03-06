import sys, getopt, os
from FileIO import FileIO
from Conversation import Conversation


def main(argv):
    inputfile = ''
    outputdir = ''

    try:
        opts, args = getopt.getopt(argv, "f:oh", ["ffile=", "odir="])
    except getopt.GetoptError:
        print('Error, check file paths and run with these options:\n'
              'Visualizer.py -f <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Visualizer.py -f <inputfile> -o <outputdir>')
            sys.exit()
        elif opt in ("-f", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg

    fileIO = FileIO()
    conversation = Conversation(fileIO.open_file(inputfile))
    # print(conversation.get_text())

    print(conversation.get_text_by_sender())


if __name__ == "__main__":
    main(sys.argv[1:])

print("End")
