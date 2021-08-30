import argparse
import getopt
import logging
import os

from report_generator_project_files import report_util
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
    print(conversation_data.get_csv())


def write_messages(outputdir: str, conversation_data: Conversation) -> None:
    output = FileIO()
    output.write_txt_file(outputdir, "All_messages.txt", conversation_data.get_messages())
    output.write_txt_file(outputdir, "Messages_by_sender.txt", conversation_data.get_messages_by_sender())
    output.write_txt_file(outputdir, "Messages_by_day.txt", conversation_data.get_by_day())
    output.write_txt_file(outputdir, "Messages_as_table.csv", conversation_data.get_csv())


def main() -> None:
    # Parse Arguments
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
        help="Pre-existing directory to put visualizations",
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

    # Analyze Data
    args = parser.parse_args()

    # Set up Logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('MessengerViz')
    logger.setLevel(logging.DEBUG)

    outputdir = args.outputdir[0] if args.outputdir else None
    if outputdir:
        file_handler = logging.FileHandler(f'{outputdir}/MessengerViz.log')
    else:
        file_handler = logging.FileHandler(f'MessengerViz.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.debug('Program called with %s', args)

    fileIO = FileIO()
    inputfile = args.inputfile[0]
    conversation = Conversation(fileIO.open_json(inputfile))
    try:
        wordlist = fileIO.open_text(args.wordlist[0])
    except TypeError:
        wordlist = None
        logger.info("Wordlist not defined. Moving on.")
    if outputdir is None:
        print_messages(conversation)
    elif os.path.isdir(outputdir):
        graph_data(outputdir, conversation, wordlist)
        write_messages(outputdir, conversation)
    else:
        logger.error('Received invalid directory specification: %s', outputdir)
        parser.print_help()
        raise getopt.GetoptError('Received invalid directory specification.')


def generate_report():
    report = report_util.Report('Facebook Messenger Data Visualization')
    section1 = report.add_section('A section')
    para1 = section1.add_paragraph()
    para1.append('Test')

    section2 = report.add_section('B section')
    para2 = section2.add_paragraph()
    para2.append('Testing')

    section3 = report.add_section('C section')
    para3 = section3.add_paragraph()
    para3.append('Tested')
    table3 = section3.add_table()
    table3.caption = 'Data listing'
    table3.set_header(['first', 'second', 'third'])
    table3.set_data([[1,2,3],[4,5,6]])
    para3.append_cross_reference(table3)
    para3.append('More words here.')


    return report


if __name__ == "__main__":
    main()
    report = generate_report()

    html_generator = report_util.HTMLReportContext("")
    html_generator.generate(report, "example")
