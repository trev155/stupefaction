"""
twitter_streaming.py

Get tweets in realtime.
"""
import tweepy

KEYPATH = "keys/auth"


class MyStreamListener(tweepy.StreamListener):
    stream_limit = 1000
    current_streamed = 0

    def on_status(self, status):
        """
        Overrides tweepy.StreamListener's on_status() method.
        This gets called every time a new tweet comes in.
        """
        print(status.text)

        self.current_streamed += 1


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

    # setup a stream listener
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

    # start streaming, tracking the query
    query = "food"
    myStream.filter(track=[query])
