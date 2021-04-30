import os
import yaml
import glob
from discord.ext import commands

import asyncio

from dotenv import load_dotenv
from app.challenge_runner import ChallengeRunner
from app.challenge import Challenge


def load_challenges(path='./app/challenges'):
    """ Loads all the yaml challengss
    """
    files = glob.glob(f'{path}/*.yaml')
    challenges=[]
    for file in files:
        if not file == f'{path}/challenge_template.yaml':
            with open(file, 'r') as fp:
                try:
                    ex = yaml.safe_load(fp)
                    timeout = int(ex['challenge']['timeout'])
                    description = ex['challenge']['description']
                    challenges.append(Challenge(description,timeout=timeout))
                except yaml.YAMLError as exp:
                    print(exp)
    return challenges

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
CHANNEL = os.getenv('CHANNEL_ID')

bot = commands.Bot(command_prefix='!')
force_stop = False
user_stats = {}

async def day_runner(cr, duration_hours=8):
    # launch duration_hours tasks for the whole day (once an hour)
    global force_stop
    global user_stats
    for t in range(duration_hours):
        users = await cr.post()
        for u in users:
            if u in user_stats:
               user_stats[u]+=1
            else:
                user_stats[u]=1
        await asyncio.sleep(60*60)
        if force_stop:
            break

@bot.event
async def on_ready():
    print('wellness bot is ready')

@bot.command(name='start', help='Starts an 8-hour challenge runner')
async def start_day(ctx):
    print(f'start day command sent by {ctx.author}')
    global force_stop
    force_stop = False
    cr = ChallengeRunner(ctx, bot)
    for challenge in load_challenges():
        cr.add_challenge(challenge)
    bot.loop.create_task(day_runner(cr))

@bot.command(name='stop', help='stop the challenge runnder')
async def stop_day(ctx):
    print(f'start day command sent by {ctx.author}')
    global force_stop
    force_stop = True
    await ctx.send("Day is over")

@bot.command(name='reset', help='reset usage challenge statistics')
async def reset(ctx):
    print(f'reset command sent by {ctx.author}')
    global user_stats
    user_stats = {}
    pass

@bot.command(name='stats', help='shows current challenge stats')
async def stats(ctx):
    print(f'stats command sent by {ctx.author}')
    global user_stats
    print(user_stats)
    msg=''
    sorted_res = sorted(user_stats.items(), key=lambda kv: kv[1], reverse=True)
    arrow = 'Congrats! -->'
    for u in sorted_res:
        msg += f'{arrow} {u[0]} has {u[1]} points\n'
        arrow = '             '

    if  msg =='':
        await ctx.send('Sorry, empty stats')
    else:
        await ctx.send(msg)

bot.run(TOKEN)
