"""
analysis_trends.py

Analysis of trends data. Input is the output from twitter_trends.py.

Input looks like:
trend_data = [
    {
        "woeid": woeid,
        "location_name": location name,
        "starting": date,
        "trend_list": list of trends
    },
    ...
]
"""
import argparse
import json
import os


def top_ten_all(trends_data, output_filepath):
    """
    Write the top 10 trends for all woeids in trends_data to the output_filepath.

    :param trends_data: list of dictionaries, containing trend data
    :param output_filepath: string, output file name to write to
    """
    with open(output_filepath, "w") as f:
        f.write("Top 10 Trends for locations in Canada\n\n")

        for location in trends_data:
            f.write("Top 10 Trends for %s (woeid %d), on %s:\n" % (location["location_name"],
                                                                   location["woeid"],
                                                                   location["starting"].split("T")[0]))
            for i in range(10):
                f.write("%d. %s\n" % (i + 1, location["trend_list"][i]))
            f.write("\n")


def unique_trending(trends_data, output_filepath):
    """
    Write unique trends for the woeids in trends_data. Write data to output_filepath.

    :param trends_data: list of dictionaries, containing trend data
    :param output_filepath: string, output file name to write to
    """
    with open(output_filepath, "w") as f:
        f.write("Unique Trending topics for locations in Canada\n\n")

        for i in range(len(trends_data)):
            location = trends_data[i]

            # set of trending for this location
            top_ten = set(location["trend_list"][:10])

            # set of trending for all other locations combined
            others_top_ten = set()
            for j in range(len(trends_data)):
                if j != i:
                    others_top_ten = others_top_ten.union(set(trends_data[j]["trend_list"][:10]))

            # get unique trends for this location
            unique = top_ten.difference(others_top_ten)

            # write out
            if len(unique) > 0:
                f.write("Unique Top 10 Trends for %s (woeid %d), on %s:\n" % (location["location_name"],
                                                                              location["woeid"],
                                                                              location["starting"].split("T")[0]))

                for elem in unique:
                    f.write(elem + "\n")
                f.write("\n")
            else:
                f.write("There were no unique trends in the top 10 trends for %s (woeid %d), on %s.\n\n" %
                        (location["location_name"], location["woeid"], location["starting"].split("T")[0]))


if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify input file path", required=True)
    parser.add_argument("-o", "--output", help="Specify output directory", required=True)
    args = parser.parse_args()

    input_filepath = args.input
    output_dir = args.output
    timestamp = input_filepath.split("-")[1]

    with open(input_filepath, "r") as input_file:
        trends_data = list(map(lambda x: json.loads(x), input_file.readlines()))

        # get a report of the top 10 trends of these locations
        top_ten_all(trends_data, os.path.join(output_dir, "trends-top10"))

        # get a report of the unique trends in these locations
        unique_trending(trends_data, os.path.join(output_dir, "trends-unique"))
