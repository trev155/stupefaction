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


def top_ten_all(trends_data, num_trends, output_filepath):
    """
    Write the top trends for all locations (woeids) in trends_data to the output_filepath.

    :param trends_data: list of dictionaries, containing trend data
    :param num_trends: number of top trends to write out for each location
    :param output_filepath: string, output file name to write to
    """
    with open(output_filepath, "w") as f:
        f.write(str("Top %d Trends for locations in Canada\n\n" % num_trends))

        for location in trends_data:
            f.write("Top %d Trends for %s (woeid %d), on %s:\n" % (num_trends, location["location_name"],
                                                                   location["woeid"],
                                                                   location["starting"].split("T")[0]))
            for i in range(num_trends):
                f.write("%d. %s\n" % (i + 1, location["trend_list"][i]))
            f.write("\n")


def unique_trending(trends_data, num_results, output_filepath):
    """
    Write unique trends for the woeids in trends_data. Write data to output_filepath.

    :param trends_data: list of dictionaries, containing trend data
    :param num_results: number of top trending entries to consider
    :param output_filepath: string, output file name to write to
    """
    with open(output_filepath, "w") as f:
        f.write("Unique Top %d trending topics for locations in Canada\n\n" % num_results)

        for i in range(len(trends_data)):
            location = trends_data[i]

            # set of trending for this location
            top = set(location["trend_list"][:num_results])

            # set of trending for all other locations combined
            others_top = set()
            for j in range(len(trends_data)):
                if j != i:
                    others_top = others_top.union(set(trends_data[j]["trend_list"][:num_results]))

            # get unique trends for this location
            unique = top.difference(others_top)

            # write out
            if len(unique) > 0:
                f.write("Unique Top 10 Trends for %s (woeid %d), on %s:\n" % (location["location_name"],
                                                                              location["woeid"],
                                                                              location["starting"].split("T")[0]))

                for elem in unique:
                    f.write(elem + "\n")
                f.write("\n")
            else:
                f.write("There were no unique trends in the top %d trends for %s (woeid %d), on %s.\n\n" %
                        (num_results, location["location_name"], location["woeid"], location["starting"].split("T")[0]))


def common_trending(trends_data, num_results, output_filepath):
    """
    For each location in trends_data, get all the common top num_results trends.
    Write data out to output_filepath.

    :param trends_data: list of dictionaries, containing trends data
    :param num_results: number of top trending entries to consider
    :param output_filepath: string, output file to write to
    """
    with open(output_filepath, "w") as f:
        f.write("Common Top %d Trending topics for locations in Canada\n" % num_results)
        all_locations = list(map(lambda d: d["location_name"], trends_data))
        f.write("All Locations Considered: ")
        for location in all_locations:
            f.write(location + ",")
        f.write("\n\n")

        # intersect all top
        if len(trends_data) == 0:
            # shouldn't happen, but handle gracefully
            f.write("No data available!")
        elif len(trends_data) == 1:
            top = trends_data[0]["trend_list"][:num_results]
            for t in top:
                f.write(t + "\n")
        else:
            common_top = set(trends_data[0]["trend_list"][:num_results])
            for i in range(1, len(trends_data)):
                top = set(trends_data[i]["trend_list"][:num_results])
                common_top = common_top.intersection(top)
            for t in common_top:
                f.write(t + "\n")


if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify input file path", required=True)
    parser.add_argument("-o", "--output", help="Specify output directory", required=True)
    args = parser.parse_args()

    input_filepath = args.input
    output_dir = args.output
    timestamp = "-".join(input_filepath.split("-")[1:])

    with open(input_filepath, "r") as input_file:
        trends_data = list(map(lambda x: json.loads(x), input_file.readlines()))

        # get a report of the top 10 trends of these locations
        top_ten_all(trends_data, 10, os.path.join(output_dir, "trends-top10" + "-" + timestamp))

        # get a report of the unique trends from top 20 in these locations
        unique_trending(trends_data, 20, os.path.join(output_dir, "trends-unique" + "-" + timestamp))

        # get a report of the common trends across locations
        common_trending(trends_data, 20, os.path.join(output_dir, "trends-common" + "-" + timestamp))
