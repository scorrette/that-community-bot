import discord

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Cute dancing snom")
    async def snom(self, ctx):
        msg = '<a:snomdance:779428824777228289>'
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Fun(bot))