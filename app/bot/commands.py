from app.exceptions.db import DbNotInitialized, ModelSchemaError
from app.db.models.challenge import Challenge
import os
import logging
from datetime import datetime
from app.db.client import Client
from discord.ext.commands import Context, Bot
from app.scheduler.runner import ChallengeRunner
from app.helpers.decorators import in_wellness_channel, log_user

_log = logging.getLogger(__name__)
bot = Bot(command_prefix='!')
runner = ChallengeRunner(bot)


@log_user
@in_wellness_channel
@bot.command(name='start', help='Schedules a set of challenges')
async def start_day(ctx: Context):
    runner.start(ctx)


@log_user
@in_wellness_channel
@bot.command(name='stop', help='Stop the challenge runner')
async def stop_day(ctx: Context):
    await ctx.send("Todays scheduled exercises have been cancelled.")


@log_user
@in_wellness_channel
@bot.command(name='shutup', help='Stop the challenge runner')
async def shutup(ctx: Context):
    await ctx.send("Ok, goodbye")


@log_user
@in_wellness_channel
@bot.command(name='challenge', help='Dispatch a challenge now')
async def challenge(ctx: Context):
    await runner.queue()


@log_user
@in_wellness_channel
@bot.command(name='reset', help='Reset challenge statistics')
async def reset(ctx: Context):
    await ctx.send("Stats reset successfully.")


@log_user
@in_wellness_channel
@bot.command(name='stats', help='View current challenge stats')
async def stats(ctx: Context):
    msg = ''
    if msg == '':
        await ctx.send('No stats are available.')
    else:
        await ctx.send(msg)


@log_user
@in_wellness_channel
@bot.command(name='add', help='Add a new exercise')
async def add(ctx: Context, description: str, timeout: int = 300):
    # populate a challenge schema and post it to the challenges collection
    _log.info("add call by %s with description: %s and timeout: %s",
              ctx.author, description, timeout)
    challenge = Challenge()
    challenge.author = str(ctx.author)
    challenge.description = description
    challenge.timeout = timeout
    challenge.created = datetime.now().isoformat()
    try:
        post_id = Client.post(challenge)
    except (ModelSchemaError, DbNotInitialized) as exc:
        _log.exception("Db insert failed with: %s", exc)
        response = "Something went wrong during a db post @cS#4658"
    else:
        response = "Thanks {}! Your exercise with id {} was added.".format(ctx.author, post_id)
    await ctx.send(response)


@bot.event
async def on_ready():
    Client.init_db()
    _log.info("wellness bot ready")


def main():
    bot.run(os.getenv('DISCORD_TOKEN'))
