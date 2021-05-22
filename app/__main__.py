import os
import yaml
import glob
import random
import asyncio
import tempfile
from pathlib import Path
from discord.ext import commands

from unqlite import UnQLite

from app.challenge import Challenge
from app.challenge_runner import ChallengeRunner
from app.decorators import in_wellness_channel

def load_random_challenge():
    """ Loads all the yaml challengss
    """
    path = str(Path(__file__).parent.joinpath('challenges'))
    files = glob.glob(f'{path}/*.yaml')
    # remove template
    files.pop(files.index(f'{path}/challenge_template.yaml'))
    file = random.choice(files)
    with open(file, 'r') as fp:
        try:
            ex = yaml.safe_load(fp)
            timeout = int(ex['challenge']['timeout'])
            description = ex['challenge']['description']
            challenge = Challenge(description,timeout=timeout)
        except yaml.YAMLError as exp:
            print(exp)
    return challenge

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')

bot = commands.Bot(command_prefix='!')


force_stop = False
user_stats = {}

db_file = tempfile.NamedTemporaryFile()
db = UnQLite(db_file.name)

# use a transaction context to lock during IO
with db.transaction():
    #create a "week-runner" collection (for store all stats)
    week_run = db.collection('week_run')
    week_run.create()



async def day_runner(cr, duration_hours=8):
    # launch duration_hours tasks for the whole day (once an hour)
    global force_stop
    global user_stats

    with db.transaction(): 
        #create a "day-runner" collection (to store daily stats)
        day_run = db.collection('day_run')
        day_run.create()
    #    week_run.add(day_run)
    #print(db)

    for t in range(duration_hours):
        users = await cr.post(load_random_challenge())
        for u in users:
            with db.transaction():
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
@in_wellness_channel
async def start_day(ctx):
    print(f'start day command sent by {ctx.author}')
    global force_stop
    force_stop = False
    cr = ChallengeRunner(ctx, bot)
    bot.loop.create_task(day_runner(cr))

@bot.command(name='stop', help='stop the challenge runnder')
@in_wellness_channel
async def stop_day(ctx):
    print(f'stop day command sent by {ctx.author}')
    global force_stop
    force_stop = True
    await ctx.send("Day is over")

@bot.command(name='shutup', help='stop the challenge runnder')
@in_wellness_channel
async def stop_day(ctx):
    print(f'shutup command sent by {ctx.author}')
    global force_stop
    force_stop = True
    await ctx.send("Ok, goodbye")

@bot.command(name='challenge', help='give a random challenge')
@in_wellness_channel
async def challenge(ctx):
    print(f'challenge command sent by {ctx.author}')
    global user_stats
    cr = ChallengeRunner(ctx, bot)
    users = await cr.post(load_random_challenge())
    for u in users:
        if u in user_stats:
            user_stats[u]+=1
        else:
            user_stats[u]=1

@bot.command(name='reset', help='reset usage challenge statistics')
@in_wellness_channel
async def reset(ctx):
    print(f'reset command sent by {ctx.author}')
    global user_stats
    user_stats = {}

@bot.command(name='stats', help='shows current challenge stats')
@in_wellness_channel
async def stats(ctx):
    print(f'stats command sent by {ctx.author}')
    global user_stats
    print(user_stats)
    msg=''
    sorted_res = sorted(user_stats.items(), key=lambda kv: kv[1], reverse=True)
    arrow = 'Congrats! -->'
    for u in sorted_res:
        msg += f'{arrow} {u[0]} has {u[1]} points\n'
        arrow = '                       '

    if  msg =='':
        await ctx.send('Sorry, empty stats')
    else:
        await ctx.send(msg)

bot.run(TOKEN)
