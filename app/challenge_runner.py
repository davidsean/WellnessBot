
import asyncio
import random
import discord
from .challenge import Challenge

class ChallengeRunner:
    """
    Runs challenges on a channel
    """
    intro = 'Wellness challenge'
    reactions = {
    'done':'🤸',
    'skipped':'😴'
    }

    def __init__(self, client, channel):
        self.client=client
        self.channel=channel
        self.message = None
        self.challenges = []

    def add_challenge(self, challenge):
        self.challenges.append(challenge)

    async def post(self):
        c = random.choice(self.challenges)
        payload = f'{ChallengeRunner.intro}. {c}'
        self.message = await self.channel.send(payload)
        await self._add_reactions()
        await asyncio.sleep(c.get_timeout())
        await self._tally()

    def get_message(self):
        return self.message

    async def _tally(self):
        self.message = await self.channel.fetch_message(self.message.id)

        if self.message is not None:
            r_done = discord.utils.find(lambda r: str(r.emoji) == ChallengeRunner.reactions['done'], self.message.reactions)

            payload="Challenge over, good job "
            async for u in r_done.users():
                if not u  == self.client.user:
                    payload = payload +" "+ str(u)
            await self.message.delete()
            await self.channel.send(payload)
            return (r_done.count)

    async def _add_reactions(self):
        if self.message is not None:
            await self.message.add_reaction(ChallengeRunner.reactions['done'])
