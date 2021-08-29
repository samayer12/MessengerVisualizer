import argparse
import getopt
import sys

from src.Conversation import Conversation
from src.FileIO import FileIO
from src.Visualizer import plot_frequency, plot_word_frequency, plot_message_type_balance


def graph_data(outputdir: str, conversation_data: Conversation, wordlist: list[str] = None) -> None:
    outputdir = FileIO.validate_directory(outputdir)

    plot_frequency(
        outputdir + "Frequency_hourly",
        "Message Frequency by Hour",
        "Frequency",
        "Hour of Day",
        conversation_data.get_by_hour(),
    )
    plot_frequency(
        outputdir + "Frequency_daily",
        "Message Frequency by Day",
        "Frequency",
        "Day of Week",
        conversation_data.get_by_day(),
    )
    plot_word_frequency(outputdir + "Frequency_words", conversation_data.get_text(), wordlist)

    message_types_by_sender = conversation_data.get_message_type_count()
    for sender in message_types_by_sender:
        plot_message_type_balance(
            outputdir + sender + "_balance",
            sender,
            list(message_types_by_sender[sender].values()),
            list(message_types_by_sender[sender].keys()),
        )


def print_messages(conversation_data: Conversation) -> None:
    print(conversation_data.get_messages())
    print(conversation_data.get_messages_by_sender())
    print(conversation_data.get_by_day())


def write_messages(outputdir: str, conversation_data: Conversation) -> None:
    output = FileIO()
    output.write_txt_file(outputdir, "All_messages.txt", conversation_data.get_messages())
    output.write_txt_file(outputdir, "Messages_by_sender.txt", conversation_data.get_messages_by_sender())
    output.write_txt_file(outputdir, "Messages_by_day.txt", conversation_data.get_by_day())


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize FB messenger data from .json files")
    parser.add_argument(
        "-i",
        "--inputfile",
        metavar="InFile",
        dest="inputfile",
        required=True,
        nargs=1,
        help=".json file containing messenger data",
    )
    parser.add_argument(
        "-o",
        "--outputdirectory",
        metavar="OutFile",
        dest="outputdir",
        default=None,
        required=False,
        nargs=1,
        help="Directory to put visualizations",
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        metavar="Wordlist",
        dest="wordlist",
        default=None,
        required=False,
        nargs=1,
        help=".txt file of words to ignore",
    )

    try:
        args = parser.parse_args()
        fileIO = FileIO()
        inputfile = args.inputfile[0]
        conversation = Conversation(fileIO.open_json(inputfile))
        outputdir = args.outputdir[0]
        try:
            wordlist = fileIO.open_text(args.wordlist[0])
        except TypeError:
            wordlist = None
            print("Wordlist not defined. Moving on.")

        graph_data(outputdir, conversation, wordlist)
        if outputdir is not None:
            write_messages(outputdir, conversation)
        else:
            print_messages(conversation)

    except getopt.GetoptError:
        print("\nERROR: Check file paths\n")
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
