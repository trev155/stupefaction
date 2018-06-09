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
go back in time that far), OR a max of 200,000 of the most recent tweets.
"""
import tweepy
import sys
import twitter_util

KEYPATH = "tweety/twitter/keys/auth"
LANG = "en"
COUNT = 100
TWEET_MODE = "extended"


def twitter_search(query, num_results):
    """
    Search using the tweepy API.
    :param query: The query to search for.
    :param num_results: The maximum number of results to return
    :return: a list of data entries
    """
    query = query + " -filter:retweets"

    # setup auth
    with open(KEYPATH, "r") as auth_file:
        auth_lines = auth_file.readlines()
        CONSUMER_KEY = auth_lines[2].strip().split("=")[1]
        CONSUMER_SECRET = auth_lines[3].strip().split("=")[1]

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
    tweet_count = 0
    all_tweets = []

    while tweet_count < num_results:
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

            # add new entries to list
            data_entries = twitter_util.search_results_to_data_entries(new_tweets)
            for entry in data_entries:
                all_tweets.append(entry)
                tweet_count += 1
                if tweet_count >= num_results:
                    break

            # update variables - the last tweet of the result set is the oldest tweet
            max_id = new_tweets[-1].id

            # print number processed so far
            print("Downloaded [%d] tweets so far." % tweet_count)

        except tweepy.TweepError as e:
            print("Something went wrong: " + str(e))
            break

    return all_tweets
