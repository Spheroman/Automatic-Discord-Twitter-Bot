import requests

import twitterapi
import discord
import json
import time

with open("setup.json", "r") as read_file:
    data = json.load(read_file)

with open("past.json", "r") as read_file:
    past = json.load(read_file)

token = data["DISCORD TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
channels = data["CHANNELS"]
sender_ids = data["USER IDS"]

buffer_last = None
message_time = time.time()
buffer_message = None
buffer_reply = None
buffer_type = None


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global buffer_last, buffer_type, buffer_message, buffer_reply, message_time
    if message.author == client.user:
        return
    if message.channel.id in channels:
        if message.author.id in sender_ids:
            idx = message.content.find('https://twitter.com')
            xidx = message.content.find('https://x.com')
            if idx >= 0 or xidx >= 0:
                buffer_message = message
                text = (message.content[:idx if idx >= 0 else xidx])[:message.find("?")]
                if text in past:
                    return
                past.append(text)
                buffer_last = twitterapi.retweet(text)
                buffer_type = "rt"
                buffer_reply = None
                message_time = time.time()
            else:
                if buffer_reply is None and time.time() - message_time < 120:
                    if message.author == buffer_message.author:
                        await message.add_reaction("💬")
                        buffer_reply = message


@client.event
async def on_reaction_add(reaction, user):
    global buffer_type, buffer_reply
    if buffer_reply is reaction.message:
        if reaction.emoji == "💬":
            if buffer_reply.author == user:
                if buffer_type == "rt":
                    twitterapi.unretweet(buffer_last.data["id"])
                    twitterapi.quote_tweet(buffer_reply.content, buffer_message.content)
                    buffer_type = None


client.run(token)
