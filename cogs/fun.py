import discord
import asyncio
import re

from pytz import timezone
from datetime import datetime, timedelta
from discord.ext import commands

async def add_counter(self, ctx, word):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM `counters` WHERE `user_id`={ctx.author.id} AND `word`='{word}'")
            
            if cur.rowcount == 0:
                await cur.execute(f"INSERT INTO `counters`(`user_id`, `word`) VALUES ({ctx.author.id}, '{word}')")
                await conn.commit()

                await ctx.send(f'`{word}` has been added to the counter list.')
            else:
                await ctx.send(f'You already have `{word}` in your counter list.')

            await cur.close()
        conn.close()

async def list_counters(self, ctx):
    word_list = ""
    counter_list = ""

    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT `word`, `count` FROM `counters` WHERE `user_id`={ctx.author.id}")
            words = await cur.fetchall()

            for i in range(len(words)):
                word_list += words[i][0]
                counter_list += str(words[i][1])
                if not i == len(words) - 1:
                    word_list += '\n'
                    counter_list += '\n'

            await cur.close()
        conn.close()

    embed = discord.Embed(title="Counter List", description="Below is a list of the words you are counting:", color=0xba60f0)
    embed.add_field(name="Words", value=word_list, inline=True)
    embed.add_field(name="Counts", value=counter_list, inline=True)
    await ctx.send(embed=embed)

async def remove_counter(self, ctx, word):
    async with self.bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f'DELETE FROM `counters` WHERE `user_id`={ctx.author.id} AND `word`=\'{word}\'')
            await conn.commit()

            await cur.close()
        conn.close()

    await ctx.send(f'`{word}` has been removed from the counter list.')

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Create a poll")
    async def poll(self, ctx):
        emojis = ['\u0031\uFE0F\u20E3', '\u0032\uFE0F\u20E3', '\u0033\uFE0F\u20E3', '\u0034\uFE0F\u20E3', '\u0035\uFE0F\u20E3',
                    '\u0036\uFE0F\u20E3', '\u0037\uFE0F\u20E3', '\u0038\uFE0F\u20E3', '\u0039\uFE0F\u20E3']

        # embed = discord.Embed(title="Create a poll", description="The bot will proceed to ask you a series of questions. There is a 60 second timeout if the author does not respond.", color=0xba60f0) 
        # embed.add_field(name="Question", value="How long would you like the poll to be open?\nPlease use the following format: #d#h#m", inline=False)
        # embed.add_field(name="Example", value="0d12h0m -> 12 hours\n2d12h0m -> 2 days and 12 hours\n0d0h30m -> 30 minutes", inline=False)
        # await ctx.send(embed=embed)

        def check(message):
            return ctx.author == message.author

        try:
            # poll_time = await self.bot.wait_for('message', timeout=60, check=check)
            # while not re.match('\d{1,}d\d{1,}h\d{1,}m', poll_time.content):
            #     await ctx.send("Incorrect time format, please try again.", delete_after=10.0)
            #     poll_time = await self.bot.wait_for('message', timeout=60, check=check)
            
            # time_vals = re.split('[dhm]+', poll_time.content)
            # end_time_delta = timedelta(days=int(time_vals[0]), hours=int(time_vals[1]), minutes=int(time_vals[2]))

            embed = discord.Embed(title=None, description="Enter a title for the poll.", color=0xba60f0)
            await ctx.send(embed=embed)
            title = await self.bot.wait_for('message', timeout=60, check=check)

            embed = discord.Embed(title=None, description="Enter a description for the poll.", color=0xba60f0)
            await ctx.send(embed=embed)
            description = await self.bot.wait_for('message', timeout=60, check=check)

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
                    else: break
                else:
                    option = await self.bot.wait_for('message', timeout=60, check=check)
                    if option.content.lower() in map(str.lower, options):
                        await ctx.send('You\'ve already entered this option, try again.', delete_after=10.0)
                    else: options.append(option.content)

            embed = discord.Embed(title=title.content, description=description.content, color=0xba60f0)

            options_body = ''
            # count_body = ''
            for i in range(len(options)):
                options_body += f'{emojis[i]} {options[i]}'
                # count_body += '0'
                if not i == len(options) - 1:
                    options_body += '\n'
                    # count_body += '\n'

            embed.add_field(name="Options", value=options_body, inline=True)
            # embed.add_field(name="Total Votes", value=count_body, inline=True)
            response = await ctx.send(embed=embed)
            for i in range(len(options)):
                await response.add_reaction(emojis[i])

            # end_time = datetime.today() + end_time_delta
        except asyncio.TimeoutError:
            await ctx.send("You took too long, cancelling.")

    @commands.command(help="Create a word counter.")
    async def counter(self, ctx, option, word = None):
        if option.lower() == 'add':
            if word == None:
                await ctx.send('This command expects a word to be passed to it.')
            else: await add_counter(self, ctx, word)
        elif option.lower() == 'list':
            await list_counters(self, ctx)
        elif option.lower() == 'remove':
            if word == None:
                await ctx.send('This command expects a word to be passed to it.')
            else: await remove_counter(self, ctx, word)
        else:
            await ctx.send('You must provide either add, list, or remove as an option.')

def setup(bot):
    bot.add_cog(Fun(bot))