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
    for role in after.roles:
        if role.id == 818549791009144892: #change new-member role ID
            channel = member.guild.get_channel('818537648515448872') #change to rules channel ID
            embed=discord.Embed(description=f"{after.mention}, welcome to Herphub! <@&479309565956063234>") #change helper role ID
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Verify(bot))