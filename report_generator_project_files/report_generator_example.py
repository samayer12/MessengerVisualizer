import report_util
import numpy as np


def generate_report(dataset):
    report = report_util.Report("Random Number Dataset Report")

    section = report.add_section("Overview")

    paragraph = section.add_paragraph()
    mean = sum(dataset) / len(dataset)
    standard_deviation = dataset.std()
    paragraph.append(
        'This project proposal builds upon an existing project that visualizes Facebook Messenger data. '
        'Source data comes from Facebook Messenger data that individuals may download from their own profile. '
        'This data is passed to a command-line utility written in Python. '
        'Reference: https://github.com/samayer12/MessengerVisualizer for the existing state of the project. '
    )

    paragraph_2 = section.add_paragraph()

    ##########################################################################
    # Alice_Balance
    ##########################################################################
    figure_1 = section.add_figure()
    figure_1.caption = "Message Balance for Sender 'Alice'"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_1.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    ##########################################################################
    # Bob_Balance
    ##########################################################################
    figure_2 = section.add_figure()
    figure_2.caption = "Message Balance for Sender 'Bob'"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_2.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    ##########################################################################
    # Global Balance
    ##########################################################################
    figure_3 = section.add_figure()
    figure_3.caption = "Message Balance for All Senders"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_3.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    paragraph_2.append_cross_reference(figure_3)
    paragraph_2.append(f" shows the histogram distribution of the numbers in the dataset. ")

    ##########################################################################
    # Frequency_daily
    ##########################################################################
    figure_4 = section.add_figure()
    figure_4.caption = "Message Frequency by Day of Week"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_4.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    ##########################################################################
    # Frequency_hourly
    ##########################################################################
    figure_5 = section.add_figure()
    figure_5.caption = "Message Frequency by Hour of Day"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_5.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    ##########################################################################
    # Frequency_words
    ##########################################################################
    figure_6 = section.add_figure()
    figure_6.caption = "Message Frequency by Word"
    # notice in the next line we access matplotlib's figure object directly
    ax = figure_6.matplotlib_figure.add_subplot(1, 1, 1)
    ax.hist(dataset)
    ##########################################################################

    ##########################################################################
    # The following code demonstrates creating a table
    ##########################################################################
    tbl_1 = section.add_table()
    tbl_1.caption = "Message Listing"

    tbl_1.set_header(["Value", "Less Than 0.3", "Has digit '3'"])
    tbl_1.set_data(zip(dataset, [x < 0.3 for x in dataset], [str(x).find('3') > -1 for x in dataset]))

    paragraph_2.append_cross_reference(tbl_1)
    paragraph_2.append(f" shows the numbers in the dataset with some other properties of these numbers. ")

    ##########################################################################
    # The following code demonstrates creating another section to the report
    ##########################################################################
    section_2 = report.add_section("More Random Data")
    paragraph_3 = section_2.add_paragraph()

    return report


if __name__ == "__main__":
    # np.random.seed(19680801)
    dataset = np.random.randn(50)
    report = generate_report(dataset)

    html_generator = report_util.HTMLReportContext("")
    html_generator.generate(report, "example")
