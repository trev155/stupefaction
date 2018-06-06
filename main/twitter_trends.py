"""
twitter_trends.py

Fetch data from the Twitter API about current trending topics on Twitter.

Right now I only search for trends in locations in Canada.
"""
import sys
import argparse
import datetime
import os
import json
import tweepy

KEYPATH = "keys/auth"
FILENAME = "trends"

if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-o", "--output", help="Specify output file path", required=True)
    args = parser.parse_args()

    output_dir = args.output
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    output_filepath = os.path.join(output_dir, FILENAME + "-" + timestamp)

    # read auth details from private key file
    with open(KEYPATH, "r") as auth_file:
        auth_lines = auth_file.readlines()
        ACCESS_TOKEN = auth_lines[0].strip().split("=")[1]
        ACCESS_SECRET = auth_lines[1].strip().split("=")[1]
        CONSUMER_KEY = auth_lines[2].strip().split("=")[1]
        CONSUMER_SECRET = auth_lines[3].strip().split("=")[1]

    # setup auth
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # get access to twitter API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if not api:
        print("Can't Authenticate")
        sys.exit(-1)

    # get available woeids that twitter keeps trending topics on
    ca_woeids = []
    available_trends = api.trends_available()
    for available_trend in available_trends:
        if available_trend["countryCode"] == "CA" and available_trend["parentid"] != 1:
            ca_woeids.append(available_trend["woeid"])

    # retrieve the trending topics for each of these woeids
    with open(output_filepath, "w") as f:
        ca_trends = []
        for woeid in ca_woeids:
            trends = api.trends_place(woeid)[0]

            trend_data = {
                "woeid": trends["locations"][0]["woeid"],
                "location_name": trends["locations"][0]["name"],
                "starting": trends["as_of"],
                "trend_list": list(map(lambda t: t["name"].lower(), trends["trends"]))
            }

            # write out to file
            f.write(json.dumps(trend_data) + "\n")
            f.flush()

    print("Completed Fetching Twitter Trends")
