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

auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secrets,
    access_token,
    access_secret
)
api = tweepy.API(auth)


def retweet(message):
    # Authenticate to Twitter
    last = ""
    for i in message.split("/"):
        last = i
    return api.retweet(last.split("?")[0])


def unretweet(tweet):
    api.unretweet(tweet)


def reply(message, tweet):
    return api.update_status(status="@PTCGDecklists " + message, in_reply_to_status_id=tweet.id)


def quote_tweet(url, message):
    return api.update_status(status=url + " " + message)


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
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False
