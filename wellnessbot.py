import os

import discord
import asyncio

from dotenv import load_dotenv
from app.challenge import Challenge

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
CHANNEL = os.getenv('CHANNEL_ID')

client = discord.Client()


async def task_runner():
    channel = client.get_channel(int(CHANNEL))
    c1 = Challenge(client, channel, 'Do 5 pushups', time=60*3, counter=1)
    #c1 = Challenge(client, channel, 'Pick 5 boogers from Vit\'s nose', 2)
    await c1.post()
    await asyncio.sleep(60)



@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.id == int(GUILD), client.guilds)
    channel = client.get_channel(int(CHANNEL))
    await channel.send('test test')

    #client.loop.create_task(task_runner())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.content == '99!':
    #     await message.channel.send('blep!')


client.run(TOKEN)
