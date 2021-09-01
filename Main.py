import argparse
import getopt
import logging
import os
from typing import List

import numpy

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


def print_messages(conversation_data: Conversation) -> List[str]:
    print(conversation_data.get_messages())
    print(conversation_data.get_messages_by_sender())
    print(conversation_data.get_by_day())
    print(conversation_data.get_csv())
    return conversation_data.get_csv()


def write_messages(outputdir: str, conversation_data: Conversation) -> None:
    output = FileIO()
    output.write_txt_file(outputdir, "All_messages.txt", conversation_data.get_messages())
    output.write_txt_file(outputdir, "Messages_by_sender.txt", conversation_data.get_messages_by_sender())
    output.write_txt_file(outputdir, "Messages_by_day.txt", conversation_data.get_by_day())
    output.write_txt_file(outputdir, "Messages_as_table.csv", conversation_data.get_csv())


def main() -> List[str]:
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
    return print_messages(conversation)


def generate_report(table_data):
    dataset = numpy.random.randn(50)
    report = report_util.Report("Facebook Messenger Data Visualization")

    section = report.add_section("Overview")

    paragraph = section.add_paragraph()
    paragraph.append(
        'This project proposal builds upon an existing project that visualizes Facebook Messenger data. '
        'Source data comes from Facebook Messenger data that individuals may download from their own profile. '
        'This data is passed to a command-line utility written in Python. '
        'Reference: https://github.com/samayer12/MessengerVisualizer for the existing state of the project. '
    )

    section2 = report.add_section('Balance Section')
    para2 = section2.add_paragraph()
    para2.append('This section describes the relative balance by content type for each sender and for the '
                 'conversation as a whole.')
    ##########################################################################
    # Alice_Balance
    ##########################################################################
    figure_1 = section2.add_figure()
    figure_1.caption = "Message Balance for Sender 'Alice'"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_1.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    para2.append_cross_reference(figure_1)
    para2.append(' shows the message balance for Alice. ')
    ##########################################################################
    # Bob_Balance
    ##########################################################################
    figure_2 = section2.add_figure()
    figure_2.caption = "Message Balance for Sender 'Bob'"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_2.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    para2.append_cross_reference(figure_2)
    para2.append(' shows the message balance for Bob. ')
    ##########################################################################
    # Global Balance
    ##########################################################################
    figure_3 = section2.add_figure()
    figure_3.caption = "Message Balance for All Senders"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_3.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    para2.append_cross_reference(figure_3)
    para2.append(' describes the message balance for all participants.')

    section3 = report.add_section('Frequency Analysis')
    para3 = section3.add_paragraph()
    para3.append('This section describes the frequency of words, and the time of day/week when messages are sent. ')
    ##########################################################################
    # Frequency_daily
    ##########################################################################
    figure_4 = section3.add_figure()
    figure_4.caption = "Message Frequency by Day of Week"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_4.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    para3.append_cross_reference(figure_4)
    para3.append(' shows the number of messages sent during each day of the week.')
    ##########################################################################
    # Frequency_hourly
    ##########################################################################
    para3.append('This sections provide time and word frequency data for the converstation. ')
    figure_5 = section3.add_figure()
    figure_5.caption = "Message Frequency by Hour of Day"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_5.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    para3.append_cross_reference(figure_5)
    para3.append(' shows the number of messages sent during each hour of the day. ')
    ##########################################################################
    # Frequency_words
    ##########################################################################
    figure_6 = section3.add_figure()
    figure_6.caption = "Message Frequency by Word"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_6.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    para3.append_cross_reference(figure_6)
    para3.append(' shows the frequency of the unique words that appeared in the conversation data.')
    ##########################################################################

    ##########################################################################
    # The following code demonstrates creating a table
    ##########################################################################
    section4 = report.add_section('Source Messages')
    para5 = section4.add_paragraph()
    table4 = section4.add_table()
    table4.caption = 'Data listing'
    table4.set_header(table_data[0])
    table4.set_data(table_data[1])
    para5.append_cross_reference(table4)
    para5.append(' contains raw source data as a table.')

    ##########################################################################
    # The following code demonstrates creating another section to the report
    ##########################################################################

    return report


if __name__ == "__main__":
    table_data = main()
    report = generate_report(table_data)

    html_generator = report_util.HTMLReportContext("")
    html_generator.generate(report, "out/Mayer_report")
