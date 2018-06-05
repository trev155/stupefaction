import html
import re
from textblob import TextBlob


#################
# Data Handling #
#################
def search_results_to_data_entries(results):
    """
    Given the results of a tweepy search(), extract the most relevant features of this data.
    Specifically, we return a list of data entries.

    :param results: SearchResults object, the return value of tweepy's, API.search()
    """
    data_entries = []
    for tweet in results:
        data_entries.append(tweet_to_data_entry(tweet))
    return data_entries


def tweet_to_data_entry(tweet):
    """
    Takes a tweet, extracts the relevant fields, and return a data entry, a light-weight version of the tweet.
    Also adds extra features from the text, run through TextBlob.

    The input data format is a "Status" object, representing a tweet. The format can be found here:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html

    The return value / data entry looks like:
    {
        "raw": raw tweet text,
        "cleaned": cleaned tweet text,
        "created_at": date the tweet was made,
        "author_num_followers": number of followers by the person who made the tweet,
        "author_num_favourites": number of favourites that the author of the tweet has,
        "hashtags": a list of hashtags contained in the tweet,
        "mentions": a list of user mentions contained in the tweet,
        "retweets": number of retweets,
        "source": platform that the tweet was made from,
        "polarity": TextBlob sentiment score, in the range of [-1, 1]. -1 is negative, 1 is positive,
        "subjectivity": TextBlob sentiment score, in the range of [0, 1]. 0 is objective, 1 is subjective,
        "tags": TextBlob PoS tagging, list of tuples
    }

    :param tweet: a single "Status" object, representing a tweet.
    :return: dictionary, data entry
    """
    # extract text from the tweet
    tweet_text = tweet._json["full_text"]
    cleaned_tweet_text = clean_tweet(tweet_text)

    # extract other metadata from the tweet
    creation_data = str(tweet.created_at)
    author_num_followers = tweet.author.followers_count
    author_num_favourites = tweet.author.favourites_count
    hashtags = list(map(lambda tag: tag["text"].lower(), tweet.entities["hashtags"]))
    mentions = list(map(lambda tag: tag["screen_name"].lower(), tweet.entities["user_mentions"]))
    retweets = tweet.retweet_count
    source = tweet.source

    # get other features from the tweet text using TextBlob
    tb = TextBlob(cleaned_tweet_text)
    polarity = tb.sentiment.polarity
    subjectivity = tb.sentiment.subjectivity
    tags = tb.tags

    # create the data entry
    data_field_names = ["raw", "cleaned", "created_at", "author_num_followers", "author_num_favourites", "hashtags",
                        "mentions", "retweets", "source", "polarity", "subjectivity", "tags"]
    data_fields = [tweet_text, cleaned_tweet_text, creation_data, author_num_followers, author_num_favourites, hashtags,
                   mentions, retweets, source, polarity, subjectivity, tags]

    data_entry = {}
    for i in range(len(data_field_names)):
        data_entry[data_field_names[i]] = data_fields[i]

    return data_entry


###################
# String Cleaning #
###################
def clean_tweet(s):
    """
    Take in a string representing the text field of a tweet, and clean it up.

    :param s: string to clean
    :return: string: cleaned string
    """
    cleaned_str = remove_retweet(s)
    cleaned_str = decode_html_char_codes(cleaned_str)
    cleaned_str = remove_hashtags(cleaned_str)
    cleaned_str = remove_urls(cleaned_str)
    cleaned_str = remove_newlines(cleaned_str)
    cleaned_str = remove_mentions(cleaned_str)
    cleaned_str = strip_whitespace(cleaned_str)
    cleaned_str = cleaned_str.lower()
    return cleaned_str


def remove_retweet(s):
    """
    If the string starts with "RT", it is a retweet, so remove that part.
    :param s: string to clean
    :return: string: cleaned string
    """
    cleaned_tweet = s
    # if the string starts with "RT" it is a retweet, so remove that part
    if s[0:2] == "RT":
        first_colon_index = s.find(":")
        cleaned_tweet = s[first_colon_index + 2:]
    return cleaned_tweet


def decode_html_char_codes(s):
    """
    Escape html character codes, such as &amp.
    :param s: string to clean
    :return: string: cleaned string
    """
    return html.unescape(s)


def remove_hashtags(s):
    """
    Remove hashtags from a string.
    Example: "#food is good" -> "food is good"

    :param s: string to clean
    :return: string: cleaned string
    """
    return s.replace("#", "")


def remove_mentions(s):
    """
    Remove mentions from a string str. Remove the entire mention, as the username is mostly irrelevant.

    Example: "Hello @bobbros okay" -> "Hello  okay"

    :param s: string to clean
    :return: string: cleaned string
    """
    return re.sub(r"\@\w+", "", s)


def remove_urls(s):
    """
    Remove urls from the string str.
    :param s: string to clean
    :return: string: cleaned string
    """
    cleaned_str = re.sub(r'http\S+', '', s)
    return cleaned_str


def remove_newlines(s):
    """
    Remove newlines from the string str.
    :param s: string to clean
    :return: string: cleaned string
    """
    return s.replace("\n", "")


def strip_whitespace(s):
    """
    Remove leading and trailing whitespace.
    :param s: string to clean
    :return: string: cleaned string
    """
    return s.strip()
