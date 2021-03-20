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
        emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

        embed = discord.Embed(title="Create a poll", description="The bot will proceed to ask you a series of questions. There is a 60 second timeout if the author does not respond.", color=0xba60f0) 
        embed.add_field(name="Question", value="How long would you like the poll to be open?\nPlease use the following format: #d#h#m", inline=False)
        embed.add_field(name="Example", value="0d12h0m -> 12 hours\n2d12h0m -> 2 days and 12 hours\n0d0h30m -> 30 minutes", inline=False)
        await ctx.send(embed=embed)

        def check(message):
            return ctx.author == message.author

        try:
            poll_time = await self.bot.wait_for('message', timeout=60, check=check)
            while not re.match('\d{1,}d\d{1,}h\d{1,}m', poll_time.content):
                await ctx.send("Incorrect time format. Please try again:")
                poll_time = await self.bot.wait_for('message', timeout=60, check=check)
            
            time_vals = re.split('[dhm]+', poll_time.content)
            end_time_delta = timedelta(days=int(time_vals[0]), hours=int(time_vals[1]), minutes=int(time_vals[2]))

            embed = discord.Embed(title=None, description="Enter between 2 to 9 options, one line at a time.\nType **done** to complete your choices.", color=0xba60f0)
            embed.add_field(name="Example", value="pie\ncake\nice cream\nfruit\n**done**", inline=False)
            await ctx.send(embed=embed)

            option = await self.bot.wait_for('message', timeout=60, check=check)
            options = [option.content]
            while len(options) < 9:
                if options[-1].lower() == 'done':
                    options.pop()
                    if len(options) < 2:
                        await ctx.send('Not enough options, quitting prematurely...')
                        return
                    else:
                        break
                else:
                    option = await self.bot.wait_for('message', timeout=60, check=check)
                    options.append(option.content)

            embed = discord.Embed(title=None, description=None, color=0xba60f0)

            body = ''
            for i in range(len(options)):
                body += f'{emojis[i]} {options[i]}'
                if not i == len(options) - 1:
                    body += '\n'

            embed.add_field(name="Options", value=body, inline=False)
            await ctx.send(embed=embed)

            end_time = datetime.today() + end_time_delta
        except asyncio.TimeoutError:
            await ctx.send("You took too long, cancelling.")

def setup(bot):
    bot.add_cog(Fun(bot))