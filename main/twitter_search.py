"""
twitter_api.py

A script that executes a Search request to the Twitter API.

Uses tweepy, see the documentation here: http://docs.tweepy.org/en/v3.6.0/api.html.
"""
import tweepy
import json
import argparse
import twitter_util

KEYPATH = "keys/auth"
LANG = "en"
COUNT = 100
TWEET_MODE = "extended"

if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-q", "--query", help="Specify the query string to use", required=True)
    args = parser.parse_args()
    query = args.query

    # read auth details from private key file
    with open(KEYPATH, "r") as auth_file:
        auth_lines = auth_file.readlines()
        ACCESS_TOKEN = auth_lines[0].strip().split("=")[1]
        ACCESS_SECRET = auth_lines[1].strip().split("=")[1]
        CONSUMER_KEY = auth_lines[2].strip().split("=")[1]
        CONSUMER_SECRET = auth_lines[3].strip().split("=")[1]

    # setup auth
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # get API object
    api = tweepy.API(auth)

    # run query
    results = api.search(q=query, lang=LANG, count=COUNT, tweet_mode=TWEET_MODE)

    # process the results
    data_entries = twitter_util.search_results_to_data_entries(results)

    # print the results
    print(json.dumps(data_entries, indent=2))

    # save the results
    # TODO
