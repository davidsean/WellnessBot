
import discord
import asyncio

class Challenge:
    intro = 'Wellness challenge'
    reactions = {
    'done':'🤸',
    'skipped':'😴'
    }

    def __init__(self, client, channel, description, time=60, counter=1):
        self.client=client
        self.channel=channel
        self.time = time
        self.description = description
        self.counter = counter
        self.message = None

        self.payload = f'{Challenge.intro} #{self.counter}. You have {self.time}s starting now to to finish this task. \n{self.description}'

    async def post(self):
        self.message = await self.channel.send(self.payload)
        await self._add_reactions()
        await asyncio.sleep(10)
        await self._tally()


    def get_message(self):
        return self.message

    async def _tally(self):
        self.message = await self.channel.fetch_message(self.message.id)

        if self.message is not None:
            r_done = discord.utils.find(lambda r: str(r.emoji) == Challenge.reactions['done'], self.message.reactions)

            payload="Good job "
            async for u in r_done.users():
                if not u  == self.client.user:
                    payload = payload +" "+ str(u)
            await self.message.delete()
            await self.channel.send(payload)
            return (r_done.count)

    async def _add_reactions(self):
        if self.message is not None:
            await self.message.add_reaction(Challenge.reactions['done'])
