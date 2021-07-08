from os import environ
import tweepy
# from sys import argv

# Getting API key
consumer_key = environ.get("CONSUMER_KEY")
consumer_secret = environ.get("CONSUMER_SECRET")
access_token = environ.get("ACCESS_TOKEN")
access_token_secret = environ.get("ACCESS_TOKEN_SECRET")

print(consumer_key)
print(consumer_secret)
print(access_token)
print(access_token_secret)


# setting API keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
tweets = api.home_timeline()

for tweet in tweets:
    print(tweet.text)
