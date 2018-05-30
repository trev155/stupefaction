import tweepy

KEYPATH = "keys/auth"

if __name__ == "__main__":
    # read auth details from file
    with open(KEYPATH, "r") as auth_file:
        auth_lines = auth_file.readlines()
        ACCESS_TOKEN = auth_lines[0].strip().split("=")[1]
        ACCESS_SECRET = auth_lines[1].strip().split("=")[1]
        CONSUMER_KEY = auth_lines[2].strip().split("=")[1]
        CONSUMER_SECRET = auth_lines[3].strip().split("=")[1]

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)

    results = api.search(q="broodwar", count=50, lang="en")

    for result in results:
        print(result.text)
        print(result.created_at)

        print("")

    print(len(results))