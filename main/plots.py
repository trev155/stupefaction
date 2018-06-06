"""
plots.py

Helper functions for plotting graphs.
"""
from textwrap import wrap
import matplotlib.pyplot as plt


def create_bar_graph(counts, num_bars, xlabel, sp_left_adj, title, output_location):
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
    :param sp_left_adj: float, number to be passed into subplots_adjust(left), because plotting sucks
    :param title: string, title of plot
    :param output_location: string, output file location for plot
    """
    # sort counts
    ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top = dict(ordered[:num_bars])

    # plot
    plt.bar(range(num_bars), list(top.values()), align='center', color="orange")
    plt.subplots_adjust(bottom=0.4, left=sp_left_adj)
    plt.title("\n".join(wrap(title, 70)))
    plt.xticks(range(num_bars), list(top.keys()), rotation=85)
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
    :param output_location: string, output file location for plot
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
    patches, texts, pcts = plt.pie(percentages_list, labels=labels_list, autopct="%.2f", explode=explode_list,
                                   startangle=90, shadow=True)
    plt.title("\n".join(wrap(title, 60)))
    plt.savefig(output_location)
    plt.close()


def create_pie_chart_fixed_pieces(counts, title, output_location):
    """
    Create a pie chart with a fixed number of slices.
    Uses all the fields in the input counts dictionary.

    The input `counts` dictionary must look like:
    {
        "str_A": int,
        "str_B": int,
        etc.
    }

    :param counts: dictionary of counts
    :param title: string, title of plot
    :param output_location: string, output file location for plot
    :return:
    """
    ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    labels_list = [kv[0] for kv in ordered]
    counts_list = [kv[1] for kv in ordered]
    total_count = sum(counts_list)
    percentages_list = list(map(lambda c: float(c) / total_count * 100, counts_list))

    explode_list = [0 for _ in range(len(counts))]
    if len(counts) > 2:
        explode_list[-2] = 0.05
        explode_list[-1] = 0.10

    # plot
    patches, texts, pcts = plt.pie(percentages_list, labels=labels_list, autopct="%.2f", explode=explode_list,
                                   startangle=90, shadow=True)
    plt.title("\n".join(wrap(title, 60)))
    plt.savefig(output_location)
    plt.close()


def create_scatter_plot(data_points, title, xlabel, ylabel, output_location):
    """
    Create a scatter plot.
    Input is a list of (x, y) tuples.

    :param data_points: list of (x, y) tuples
    :param title: string, title of plot
    :param xlabel: string, x-axis label
    :param ylabel: string, y-axis label
    :param output_location: string, output file location for plot
    """
    x = list(map(lambda e: e[0], data_points))
    y = list(map(lambda e: e[1], data_points))

    # plot
    plt.scatter(x, y, alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("\n".join(wrap(title, 60)))
    plt.savefig(output_location)
    plt.close()
