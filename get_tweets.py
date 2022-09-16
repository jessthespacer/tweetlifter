import tweepy
import os
import pandas as pd
from pathlib import Path

saveto = Path(r"C:\Users\jinsi\GitHub\tweetlifter\Data") / 'tweet_dump.csv'

# Set up authentication
BEARER_TOKEN = os.environ.get("TW_BEARER_TOKEN")
CONSUMER_KEY = os.environ.get("TW_API_KEY")
CONSUMER_SECRET = os.environ.get("TW_API_SECRET")
ACCESS_TOKEN = os.environ.get("TW_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TW_ACCESS_SECRET")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Pull tweets from user
username = "WesternWeightRm"
user = client.get_user(username=username).data

paginator = tweepy.Paginator(
    client.get_users_tweets,
    user.id,
    exclude=["retweets", "replies"],
    tweet_fields="created_at",
    max_results=100
)

tweets = []
for resp in paginator:
    tweets += resp.data

# Save to CSV
tweet_id = []
tweet_created = []
tweet_data = []

for tweet in tweets:
    tweet_id.append(tweet.id)
    tweet_created.append(tweet.created_at)
    tweet_data.append(tweet.text)

d = {'tweet_id': tweet_id, 'tweet_created': tweet_created, 'tweet_data': tweet_data}

df = pd.DataFrame(d)

try:
    df.to_csv(saveto)
except FileNotFoundError:
    print("ERROR: Could not find directory indicated. Attempting save instead to", Path().absolute() / "tweet_dump.csv")
    df.to_csv("tweet_dump.csv")

print("Pulled and saved", len(df), "tweets from the ungodly bird app.")