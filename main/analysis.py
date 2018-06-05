"""
analysis.py

Read in the output from twitter_search.py, and run some analytics, plot some graphs, etc.
"""
import argparse
import json
import os
from textwrap import wrap
import matplotlib.pyplot as plt


FILE_DELIMITER_CHAR = "|"

###########
# Helpers #
###########
def get_hashtag_counts(data_entries):
    """
    Count the number of occurrences of every hashtag in data_entries.
    :param data_entries: list of data entries
    :return: dictionary of counts
    """
    counts = {}
    for entry in data_entries:
        for hashtag in entry["hashtags"]:
            if hashtag in counts:
                counts[hashtag] += 1
            else:
                counts[hashtag] = 1
    return counts


def get_source_counts(data_entries):
    """
    Count the number of each source for every entry in data_entries.
    :param data_entries: list of data entries
    :return: dictionary of counts
    """
    counts = {}
    for entry in data_entries:
        source = entry["source"]
        if source in counts:
            counts[source] += 1
        else:
            counts[source] = 1
    return counts


#################
# Plots, Graphs #
#################
def create_bar_graph(counts, num_bars, xlabel, title, output_location):
    """
    Create and plot a bar graph of frequencies for the counts.

    The input `counts` dictionary must look like:
    {
        "str_A": int,
        "str_B": int,
        etc.
    }

    :param counts: dictionary of counts
    :param num_bars: number of bars on the x-axis
    :param xlabel: string, label for x-axis
    :param title: string, title of plot
    :param output_location: string, output file location for plot
    """
    # sort counts
    ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top = dict(ordered[:num_bars])

    # plot
    plt.bar(range(num_bars), list(top.values()), align='center', color="orange")
    plt.gcf().subplots_adjust(bottom=0.3)
    plt.title("\n".join(wrap(title, 70)))
    plt.xticks(range(num_bars), list(top.keys()), rotation=70)
    plt.xlabel(xlabel)
    plt.ylabel(s="frequency")
    plt.savefig(output_location)
    plt.close()


def create_pie_chart(counts, num_parts, title, output_location):
    """
    Create and plot a pie chart for counts.

    The input `counts` dictionary must look like:
    {
        "str_A": int,
        "str_B": int,
        etc.
    }

    :param counts: dictionary of counts
    :param num_parts: number of pie parts
    :param title: string, title of plot
    :param: output_location: string, output file location for plot
    """
    # figure out how to split the pie
    ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    labels_list = [kv[0] for kv in ordered[:num_parts - 1]] + ["Others"]

    counts_list = [kv[1] for kv in ordered[:num_parts - 1]]
    total_count = sum([kv[1] for kv in ordered])
    others = total_count - sum(counts_list)
    counts_list.append(others)

    percentages_list = list(map(lambda c: float(c) / total_count * 100, counts_list))

    explode_list = [0 for _ in range(num_parts)]
    if num_parts > 6:
        explode_list[-4] = 0.10
        explode_list[-3] = 0.10
        explode_list[-2] = 0.10
        explode_list[-1] = 0.10

    # plot
    patches, texts, pcts = plt.pie(percentages_list, labels=labels_list, autopct="%.2f", explode=explode_list, startangle=90, shadow=True)
    plt.title("\n".join(wrap(title, 60)))
    plt.savefig(output_location)
    plt.close()


def title_builder(main, query, date):
    """
    Build a string for a plot title.

    :param main: Main substance of the title.
    :param query: the query used
    :param date: timestamp
    :return: string
    """
    return main + ", for the search query '" + query + "', " + "for the last 7 days starting at (" + date + ")"


if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify input file path", required=True)
    parser.add_argument("-o", "--output", help="Specify output file path", required=True)
    args = parser.parse_args()

    input_filepath = args.input

    # retrieve the original query used in the search
    basename = os.path.basename(input_filepath)

    query_list = basename.split(FILE_DELIMITER_CHAR)[:-1]
    query_used = " ".join(query_list)

    # retrieve the timestamp
    timestamp = basename.split(FILE_DELIMITER_CHAR)[-1]

    # determine where output files should be placed
    output_filepath = os.path.join(args.output, basename)

    with open(input_filepath, "r") as input_file:
        # read in data as a list of dictionaries
        data_entries = list(map(lambda e: json.loads(e), input_file.readlines()))

        # pie chart of source frequencies
        source_counts = get_source_counts(data_entries)
        create_pie_chart(source_counts, 7, title_builder("Source of Tweets", query_used, timestamp),
                         output_filepath + "-" + "sources")

        # bar graph of hashtag frequencies
        hashtag_counts = get_hashtag_counts(data_entries)
        create_bar_graph(hashtag_counts, 12, "Hashtags",
                         title_builder("Hashtag frequencies", query_used, timestamp),
                         output_filepath + "-" + "hashtags")

