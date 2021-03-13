import discord

from discord.ext import commands

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()
async def on_raw_reaction_add(self, payload):
    channel = await self.bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = channel.guild.get_member(payload.user_id)
    emoji = payload.emoji

def setup(bot):
    bot.add_cog(Verify(bot))