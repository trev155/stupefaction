"""
twitter_api.py

Accessing the twitter api and processing data.
"""
import tweepy
import tweet_cleaning
import json

from textblob import TextBlob

KEYPATH = "keys/auth"


def process_results(results):
    data_entries = []
    for tweet in results:
        data_entries.append(tweet_to_data_entry(tweet))
    print(json.dumps(data_entries, indent=2))


def tweet_to_data_entry(tweet):
    """
    Takes a tweet, extracts the relevant fields, returns a light-weight version of the tweet.
    Also adds extra features from the text, run through TextBlob.

    :param tweet:
    :return: dictionary, data entry
    """
    # extract text from the tweet
    tweet_text = tweet._json["full_text"]
    cleaned_tweet_text = tweet_cleaning.clean_tweet(tweet_text)

    # extract other metadata from the tweet
    creation_data = str(tweet.created_at)
    author_num_followers = tweet.author.followers_count
    author_num_favourites = tweet.author.favourites_count
    hashtags = list(map(lambda tag: tag["text"], tweet.entities["hashtags"]))
    mentions = list(map(lambda tag: tag["screen_name"], tweet.entities["user_mentions"]))
    retweets = tweet.retweet_count
    source = tweet.source

    # get other features from the tweet text using TextBlob
    tb = TextBlob(cleaned_tweet_text)
    polarity = tb.sentiment.polarity
    subjectivity = tb.sentiment.subjectivity
    tags = tb.tags

    # create the data entry
    data_field_names = ["text", "created_at", "author_num_followers", "author_num_favourites", "hashtags", "mentions",
                   "retweets", "source", "polarity", "subjectivity", "tags"]
    data_fields = [cleaned_tweet_text, creation_data, author_num_followers, author_num_favourites, hashtags,
                   mentions, retweets, source, polarity, subjectivity, tags]
    data_entry = {}
    for i in range(len(data_field_names)):
        data_entry[data_field_names[i]] = data_fields[i]

    return data_entry


if __name__ == "__main__":
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
    results = api.search(q="#cnn", lang="en", count=50, tweet_mode="extended")

    process_results(results)
