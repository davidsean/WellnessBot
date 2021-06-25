
import asyncio
import logging
import discord
from typing import Optional
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from app.db.client import Client
from app.db.models.challenge import Challenge
from app.exceptions.db import NullQueryResult


class ChallengeRunner:
    """
    Runs challenges on a channel
    """
    reactions = {
        'done': '🤸',
        'skipped': '😴'
    }

    def __init__(self, ctx: Context, bot: Bot):
        self._log = logging.getLogger(__name__)
        self.ctx = ctx
        self.bot = bot
        self.challenges = []

    async def _post(self, payload: str) -> Message:
        message: Message = await self.ctx.send(payload)
        self._log.info("Post successful with content: %s", message.content)
        return message

    async def post_challenge(self) -> Optional[list]:
        challenge = self.load_challenge()
        if challenge is None:
            await self._post("No challenges available")
            return
        payload = "@here Incoming Wellness Challenge!\
            \nYou have {} seconds to finish this task.{}".format(
            challenge.timeout, challenge.description)
        message: Message = await self._post(payload)
        await self._add_reactions(message)
        await asyncio.sleep(challenge.timeout)
        users = await self._tally(message)
        return users

    async def _tally(self, message: Message) -> list:
        # get the new message including reactions
        message = await self.ctx.fetch_message(message.id)
        user_str = []
        # find the done reaction in the message
        r_done = discord.utils.find(lambda r: str(
            r.emoji) == ChallengeRunner.reactions['done'], message.reactions)
        payload = "Challenge over, good job "
        if r_done is None:
            await message.delete()
            await self.ctx.send(payload)
            return user_str
        async for u in r_done.users():
            if not u == self.bot.user:
                payload = payload + " " + str(u)
                user_str.append(str(u))
        await message.delete()
        await self.ctx.send(payload)
        return user_str

    async def _add_reactions(self, message: Message):
        await message.add_reaction(ChallengeRunner.reactions['done'])
        await message.add_reaction(ChallengeRunner.reactions['skipped'])

    def load_challenge(self) -> Optional[Challenge]:
        challenge = None
        try:
            challenge = Client.get(Challenge())
        except NullQueryResult as exc:
            self._log.exception(exc)
        return challenge

    async def day_runner(self, duration_hours=8):
        for t in range(duration_hours):
            challenge = self.load_challenge()
            if challenge is None:
                await self._post("No challenges available")
            else:
                users = await self.post_challenge()
                # for u in users:
                #     if u in user_stats:
                #         user_stats[u] += 1
                #     else:
                #         user_stats[u] = 1
                await asyncio.sleep(60 * 60)
