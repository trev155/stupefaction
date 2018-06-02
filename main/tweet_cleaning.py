import html
import re


def clean_tweet(str):
    """
    Take in a string representing the text field of a tweet, and clean it up.

    :param str: string to clean
    :return: str: cleaned string
    """
    cleaned_str = remove_retweet(str)
    cleaned_str = decode_html_char_codes(cleaned_str)
    cleaned_str = remove_hashtags(cleaned_str)
    cleaned_str = remove_urls(cleaned_str)
    cleaned_str = remove_newlines(cleaned_str)
    cleaned_str = remove_mentions(cleaned_str)
    cleaned_str = strip_whitespace(cleaned_str)
    return cleaned_str


def remove_retweet(str):
    """
    If the string starts with "RT", it is a retweet, so remove that part.
    :param str: string to clean
    :return: str: cleaned string
    """
    cleaned_tweet = str
    # if the string starts with "RT" it is a retweet, so remove that part
    if str[0:2] == "RT":
        first_colon_index = str.find(":")
        cleaned_tweet = str[first_colon_index + 2:]
    return cleaned_tweet


def decode_html_char_codes(str):
    """
    Escape html character codes, such as &amp.
    :param str: string to clean
    :return: str: cleaned string
    """
    return html.unescape(str)


def remove_hashtags(str):
    """
    Remove hashtags from a string.
    Example: "#food is good" -> "food is good"

    :param str: string to clean
    :return: str: cleaned string
    """
    return str.replace("#", "")


def remove_mentions(str):
    """
    Remove mentions from a string str. Remove the entire mention, as the username is mostly irrelevant.

    Example: "Hello @bobbros okay" -> "Hello  okay"

    :param str: string to clean
    :return: str: cleaned string
    """
    return re.sub(r"\@\w+", "", str)


def remove_urls(str):
    """
    Remove urls from the string str.
    :param str: string to clean
    :return: str: cleaned string
    """
    cleaned_str = re.sub(r'https?:\/\/.*[\r\n]*', '', str)
    return cleaned_str


def remove_newlines(str):
    """
    Remove newlines from the string str.
    :param str: string to clean
    :return: str: cleaned string
    """
    return str.replace("\n", "")


def strip_whitespace(str):
    """
    Remove leading and trailing whitespace.
    :param str: string to clean
    :return: str: cleaned string
    """
    return str.strip()
