import discord

from discord.ext import commands
from datetime import datetime
from time import perf_counter
from pkg.queries import set_counter, update_counter, remove_counter

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.uptime_start = datetime.now()

    @commands.command(help="Check the bots uptime")
    async def uptime(self, ctx):
        uptime_now = datetime.now()
        minutes, seconds = divmod((uptime_now - self.uptime_start).total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f'Up for {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {round(seconds, 2)} seconds')
    
    @commands.command(help="Latency check for the bot")
    async def ping(self, ctx):
        api_time = round(self.bot.latency * 1000, 2)

        now = perf_counter()
        response = await ctx.send(f'Pong! API time {api_time} ms.')
        response_time = round((perf_counter() - now) * 1000, 2)

        await response.edit(content=response.content + f' Response time {response_time} ms.')

    @commands.command(help="Track what you say")
    async def counter(self, ctx, op, word):
        if op.lower() == 'add':
            set_counter(ctx, word)
        elif op.lower() == 'remove':
            remove_counter(ctx, word)
        else:
            await ctx.send('First parameter must be either `add` or `remove`.')

    @counter.error
    async def counter_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Usage: `e!counter add/remove <word>`')

def setup(bot):
    bot.add_cog(Info(bot))