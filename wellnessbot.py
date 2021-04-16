import os
import yaml
import glob
import discord
import asyncio

from dotenv import load_dotenv
from app.challenge_runner import ChallengeRunner
from app.challenge import Challenge

def load_challenges(path='./app/challenges'):
    files = glob.glob(f'{path}/*.yaml')
    challenges=[]
    for file in files:
        if not file == f'{path}/challenge_template.yaml':
            with open(file, 'r') as fp:
                try:
                    ex = yaml.safe_load(fp)
                    timeout = ex['challenge']['timeout']
                    description = ex['challenge']['description']
                    challenges.append(Challenge(description,timeout=timeout))
                except yaml.YAMLError as exp:
                    print(exp)
    return challenges

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
CHANNEL = os.getenv('CHANNEL_ID')

client = discord.Client()

async def task_runner(cr):
    await cr.post()
    await asyncio.sleep(60*60)


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.id == int(GUILD), client.guilds)
    channel = client.get_channel(int(CHANNEL))
    cr = ChallengeRunner(client, channel)
    for challenge in load_challenges():
        cr.add(challenge)
    client.loop.create_task(task_runner(cr))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.content == '99!':
    #     await message.channel.send('blep!')


client.run(TOKEN)
