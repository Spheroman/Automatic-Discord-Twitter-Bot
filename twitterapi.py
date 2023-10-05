import os
import json
import tweepy
import requests

# API keys that you saved earlier
with open("setup.json", "r") as read_file:
    data = json.load(read_file)
api_key = data["API KEY"]
api_secrets = data["API SECRETS"]
access_token = data["ACCESS TOKEN"]
access_secret = data["ACCESS SECRET"]

client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secrets,
    access_token=access_token,
    access_token_secret=access_secret
)

auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secrets,
    access_token,
    access_secret
)
api = tweepy.API(auth)


def retweet(message):
    return client.create_tweet(text=message)

def unretweet(tweet):
    return client.delete_tweet(tweet)


def reply(message, tweet):
    return api.update_status(status="@PTCGDecklists " + message, in_reply_to_status_id=tweet.id)


def quote_tweet(url, message):
    return client.create_tweet(text=url + " " + message)


def tweet_image(urls, message):
    media_id = []
    for url in urls:
        filename = 'temp.jpg'
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            media_id.append(api.media_upload(filename=filename).media_id_string)
            os.remove(filename)
        else:
            print("Unable to download image")
    return api.update_status(status=message, media_ids=media_id)


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    if not image_url.startswith("http"):
        return False
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False
