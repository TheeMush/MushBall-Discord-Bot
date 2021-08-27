import discord
from discord.ext import commands, tasks
from itertools import cycle

class status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status = cycle(['with everyones money','Join My Server: dsc.gg/mushballhell'])

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.change_status.start()

def setup(client):
    client.add_cog(status(client))