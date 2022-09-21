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

buffer_last = None
buffer_message = None
buffer_reply = None
buffer_type = None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global buffer_last, buffer_type, buffer_message, buffer_reply
    if message.author == client.user:
        return
    if message.channel.id in channels:
        if message.author.id in sender_ids:
            if message.attachments:
                buffer = []
                for attachment in message.attachments:
                    if 'image' in attachment.content_type:
                        buffer.append(attachment)
                buffer_last = twitterapi.tweet_image(buffer, "")
                buffer_type = "img"
                buffer_reply = None
            else:
                idx = message.content.find('https://twitter.com')
                if idx >= 0:
                    buffer_message = message.content
                    buffer_last = twitterapi.retweet(message.content)
                    buffer_type = "rt"
                    buffer_reply = None
                else:
                    if buffer_reply is None:
                        await message.add_reaction("💬")
                        buffer_reply = message


@client.event
async def on_reaction_add(reaction, user):
    global buffer_type, buffer_reply
    if buffer_reply is reaction.message:
        if reaction.emoji == "💬":
            if buffer_reply.author == user:
                if buffer_type == "img":
                    twitterapi.reply(buffer_reply.content, buffer_last)
                    buffer_type = None
                if buffer_type == "rt":
                    twitterapi.unretweet(buffer_last.id)
                    twitterapi.quote_tweet(buffer_reply.content, buffer_message)
                    buffer_type = None



client.run(token)
