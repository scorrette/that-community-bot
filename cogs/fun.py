import discord

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Create a poll")
    async def poll(self, ctx):
        await ctx.send('Enter how long the poll should be open (h for hours, m for minutes, s for seconds. Ex: 1h30m, 10m, etc.):')
        poll_time = await self.bot.wait_for('message', timeout=30)
        await ctx.send(poll_time)

def setup(bot):
    bot.add_cog(Fun(bot))