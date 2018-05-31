"""
twitter_api.py

Wrapper for twitter API access.
"""
import tweepy

KEYPATH = "keys/auth"


if __name__ == "__main__":
    # read auth details from private keyfile
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
    results = api.search(q="broodwar", count=50, lang="en")

    for result in results:
        print(result.text)
        print("")
