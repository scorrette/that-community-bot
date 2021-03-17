import discord
import re

from discord.ext import commands
from datetime import datetime
from pytz import timezone
from time import perf_counter

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

    @commands.command(help="Lookup a members info")
    async def info(self, ctx, name = None):
        member = None
        # if none assume the user wants info about themselves
        if name == None:
            member = ctx.author
        elif name[0:2] == '<@' and name[-1] == '>':
            member = ctx.guild.get_member(int(name[3:-1]))
        elif re.match('#\d{4}', name[-5:]):
            member = ctx.guild.get_member_named(name)
        else:
            for guild_member in ctx.guild.members:
                if(re.search(name, guild_member.name, re.IGNORECASE) or
                   (not guild_member.nick == None and 
                    re.search(name, guild_member.nick, re.IGNORECASE))):
                    member = guild_member
                    break

        if member == None:
            await ctx.send("User was not found.")
            return

        roles = ''
        role_count = 0

        for i in range(len(member.roles)):
            role = member.roles[i]

            if not role.name == '@everyone':
                roles += role.name
                role_count += 1

            if role_count <= (len(member.roles) - 2) and role_count > 0:
                roles += ', '

        embed = discord.Embed(title=None, description=None, color=0xba60f0) 
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="Account Created", value=member.created_at.astimezone(timezone('US/Eastern')).strftime('%x %X %Z'), inline=False)
        embed.add_field(name="Join Date", value=member.joined_at.astimezone(timezone('US/Eastern')).strftime('%x %X %Z'), inline=False)
        if len(member.roles) == 1:
            embed.add_field(name=f'Roles [0]', value="No roles", inline=False)
        else:
            embed.add_field(name=f'Roles [{(len(member.roles) - 1)}]', value=roles, inline=False)
        embed.set_author(name=str(member), icon_url=str(member.avatar_url))
        embed.set_thumbnail(url=str(member.avatar_url))

        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        await ctx.send(f'Something unexpected occurred: {error}')

def setup(bot):
    bot.add_cog(Info(bot))