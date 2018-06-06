"""
twitter_search.py

A script that executes a Search request to the Twitter API.

Uses tweepy, see the documentation here: http://docs.tweepy.org/en/v3.6.0/api.html.
Credit to: https://dev.to/bhaskar_vk/how-to-use-twitters-search-rest-api-most-effectively

The script takes in a search query, in the "query" argument.
This string may be space separated and contain multiple search terms, such as:
'hello world' or '"watching now"'.

The script produces an output file with the query term, as well as a timestamp.
The output file contains all the tweets that match the query from the past 7 days (as the twitter API only lets you
go back in time that far), OR a max of 500,000 of the most recent tweets.
"""
import tweepy
import argparse
import sys
import os
import json
import datetime
import twitter_util

KEYPATH = "keys/auth"
LANG = "en"
COUNT = 100
MAX_TWEETS = 200000
TWEET_MODE = "extended"
FILE_DELIMITER_CHAR = "|"

if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-q", "--query", help="Specify the query string to use", required=True)
    parser.add_argument("-o", "--output", help="Specify output file path", required=True)
    args = parser.parse_args()

    # the input query is some space separated string
    raw_query = args.query
    raw_query_list = raw_query.split(" ")

    # generate a non-space string representation of the raw query
    raw_query_with_no_spaces = FILE_DELIMITER_CHAR.join(raw_query_list)

    # construct the output filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    output_filepath = os.path.join(args.output, raw_query_with_no_spaces + FILE_DELIMITER_CHAR + timestamp)

    # construct the actual query that we will be using - want to ignore retweets
    query = raw_query + " -filter:retweets"

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

    # helper variables
    # all tweets have an id > 0, where higher ids are further back in time
    # initialize max_id at -1 because we don't know where to start our search
    max_id = -1
    tweetCount = 0

    with open(output_filepath, 'w') as f:
        while tweetCount < MAX_TWEETS:
            try:
                # first iteration - read the most recent tweets
                if max_id <= 0:
                    new_tweets = api.search(q=query, count=COUNT, tweet_mode='extended')
                # subsequent iterations - start searching where the previous iteration left off
                else:
                    new_tweets = api.search(q=query, count=COUNT, max_id=str(max_id - 1), tweet_mode='extended')

                # no more tweets found, exit
                if not new_tweets:
                    print("No more tweets found, exiting.")
                    break

                # save all these tweets to file
                data_entries = twitter_util.search_results_to_data_entries(new_tweets)
                for entry in data_entries:
                    f.write(json.dumps(entry) + '\n')
                f.flush()

                # update variables - the last tweet of the result set is the oldest tweet
                max_id = new_tweets[-1].id
                tweetCount += len(new_tweets)

                # print number processed so far
                print("Downloaded [%d] tweets so far." % tweetCount)

            except tweepy.TweepError as e:
                print("Something went wrong: " + str(e))
                break

    print("Downloaded [%d] tweets. Saved to %s" % (tweetCount, output_filepath))
