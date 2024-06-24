import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
API_KEY = os.getenv('TWITTER_CONSUMER_KEY')
API_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

def get_tweet_info(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    headers = create_headers(BEARER_TOKEN)
    params = {
        "tweet.fields": "created_at,author_id,public_metrics,text"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        tweet = response.json()
        print("Tweet ID:", tweet["data"]["id"])
        print("Tweet Text:", tweet["data"]["text"])
        print("Tweet Created At:", tweet["data"]["created_at"])
        print("Tweet Author ID:", tweet["data"]["author_id"])
        print("Tweet Retweet Count:", tweet["data"]["public_metrics"]["retweet_count"])
        print("Tweet Reply Count:", tweet["data"]["public_metrics"]["reply_count"])
        print("Tweet Like Count:", tweet["data"]["public_metrics"]["like_count"])
        print("Tweet Quote Count:", tweet["data"]["public_metrics"]["quote_count"])
    else:
        print(f"Error: {response.status_code} - {response.json()}")

tweet_id = "1804582276275327063"
get_tweet_info(tweet_id)