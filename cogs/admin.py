import discord

from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Modify server prefixes")
    async def prefix(self, ctx, option, prefix = None):
        if option.lower() == 'add':
            if prefix == None:
                await ctx.send('This command expects a prefix to be passed to it.')
        elif option.lower() == 'list':
            print('bad')
        elif option.lower() == 'remove':
            if prefix == None:
                await ctx.send('This command expects a prefix to be passed to it.')
        else:
            print('bad')

def setup(bot):
    bot.add_cog(Admin(bot))