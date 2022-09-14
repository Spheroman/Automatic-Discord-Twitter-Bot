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

client = tweepy.Client(consumer_key=api_key,
                       consumer_secret=api_secrets,
                       access_token=access_token,
                       access_token_secret=access_secret)


def main(message):
    # Authenticate to Twitter
    last = ""
    for i in message.split("/"):
        last = i
    client.retweet(last.split("?")[0])


def tweet_image(url, message):
    auth = tweepy.OAuth1UserHandler(
       api_key,
       api_secrets,
       access_token,
       access_secret
    )

    api = tweepy.API(auth)

    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        media = api.media_upload(filename=filename)
        api.update_status(status=message, media_ids=[media.media_id_string])
        os.remove(filename)
    else:
        print("Unable to download image")
