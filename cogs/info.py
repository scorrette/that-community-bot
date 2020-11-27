import discord

from discord.ext import commands
from datetime import datetime

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.uptime_start = datetime.now()

    @commands.command(help="Check the bots uptime")
    async def uptime(self, ctx):
        uptime_now = datetime.now()
        minutes, seconds = divmod((uptime_now - self.uptime_start).total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f'Up for {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {seconds:.{2}f} seconds')

def setup(client):
    client.add_cog(Info(client))