import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(help="Cute dancing snom")
    async def snom(self, ctx):
        msg = '<a:snomdance:779428824777228289>'
        await ctx.send(msg)

def setup(client):
    client.add_cog(Fun(client))