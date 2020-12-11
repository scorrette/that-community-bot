import discord

from discord.ext import commands
from pkg.queries import update_prefix

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Change the prefix of this bot on your server")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        success = update_prefix(ctx, prefix)
    
        if success:
            msg = "Successfully changed prefix to `" + prefix + "`"
        else:
            msg = "There was an issue changing the prefix."

        await ctx.send(msg)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            msg = ":x: You do not have permission to do that!"
            await ctx.send(msg)
        elif isinstance(error, commands.NoPrivateMessage):
            msg = ":x: You can't use that command in my DMs!"
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(Admin(bot))