from keys import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
from sys import argv, exit

# setting API keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:
    tweet = argv[1]
    api.update_status(tweet)
    print(f"Tweeted Successfully:\n\"{tweet}\"")

except IndexError:
    exit('Usage: python twtcl.py "TWEET".')

except tweepy.error.TweepError:
    exit('Error: tweet needs to be shorter.')
