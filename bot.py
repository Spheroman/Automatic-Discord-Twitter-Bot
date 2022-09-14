import twitterapi
import discord
import json

with open("setup.json", "r") as read_file:
    data = json.load(read_file)

token = data["DISCORD TOKEN"]


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
channels = data["CHANNELS"]
sender_ids = data["USER IDS"]


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id in channels:
        if message.author.id in sender_ids:
            if message.attachments is not None:
                if 'image' in message.attachments[0].content_type:
                    retweet.tweet_image(message.attachments[0].url, "")
            else:
                idx = message.content.find('https://twitter.com')
                if idx >= 0:
                    retweet.main(message.content)


client.run(token)
