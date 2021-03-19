import discord
import asyncio
import re

from pytz import timezone
from datetime import datetime, timedelta
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Create a poll")
    async def poll(self, ctx):
        embed = discord.Embed(title="Create a poll", description="The bot will proceed to ask you a series of questions. There is a 30 second timeout if the author does not respond.", color=0xba60f0) 
        embed.add_field(name="Question 1", value="How long would you like the poll to be open?\nPlease use the following format: #d#h#m", inline=False)
        embed.add_field(name="Example", value="0d12h0m -> 12 hours\n2d12h0m -> 2 days and 12 hours\n0d0h30m -> 30 minutes", inline=False)
        await ctx.send(embed=embed)

        def check(message):
            return ctx.author == message.author

        try:
            poll_time = await self.bot.wait_for('message', timeout=30, check=check)
            while not re.match('\d{1,}d\d{1,}h\d{1,}m', poll_time.content):
                await ctx.send("Incorrect time format. Please try again:")
                poll_time = await self.bot.wait_for('message', timeout=30, check=check)
            
            time_vals = re.split('[dhm]+', poll_time.content)
            end_time_delta = timedelta(days=int(time_vals[0]), hours=int(time_vals[1]), minutes=int(time_vals[2]))
            await ctx.send(datetime.today() + end_time_delta)
        except asyncio.TimeoutError:
            await ctx.send("You took too long, cancelling.")

def setup(bot):
    bot.add_cog(Fun(bot))