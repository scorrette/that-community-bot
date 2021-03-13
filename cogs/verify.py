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

@commands.Cog.listener()
async def on_member_join(member):
    channel = member.guild.get_channel('818537648515448872') #change logging channel ID
    embed=discord.Embed(description=f"{member.mention} joined the server") #change helper role ID
    await channel.send(embed=embed)

@commands.Cog.listener()
async def on_member_remove(member):
    channel = member.guild.get_channel('818537648515448872') #change logging channel ID
    embed=discord.Embed(description=f"{member.mention} left the server") #change helper role ID
    await channel.send(embed=embed)

@commands.Cog.listener()
async def on_raw_reaction_add(reaction, member):
    if reaction.emoji == 'thumbsup' and reaction.message.channel.id == 818537648515448872: #change to rules channel ID 
        member.add_role(818549791009144892, reason=None, atomic=True) #change role ID

@commands.Cog.listener()
async def on_member_update(before, after):
    role = after.guild.get_role(818549791009144892) #change member role ID
    if role in before.roles:
        return
    elif role in after.roles:
        channel = after.guild.get_channel(818537648515448872) #change verification channel ID
        embed=discord.Embed(description=f"{after.mention}, welcome to Herphub! <@&479309565956063234>") #change helper role ID
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Verify(bot))